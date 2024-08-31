import xml.etree.ElementTree as ET
from xml.dom import minidom
from mstk.forcefield.forcefield import ForceField
from mstk.forcefield.ffterm import *
from mstk import logger


class Zfp:
    '''
    Load ForceField from ZFP file.

    ZFP is the default format for storing ForceField in mstk.
    XML language is used by ZFP file to serialize the setting and all the FFTerms in a ForceField object.

    In ZFP file, there is no leading 1/2 for harmonic energy terms.
    The length is in unit of nm, and angle is in unit of degree.
    The energies for harmonic bond, harmonic angle and vdW are in unit of kJ/mol/nm^2, kJ/mol/rad^2 and kJ/mol.

    A force field term describing one topology element should only appear once.
    If there are duplicated terms, an Exception will be raised.
    e.g. HarmonicAngleTerm('c_4', 'c_4', 'h_1') and SDKAngleTerm('c_4', 'c_4', 'h_1') are considered as duplicated,
    because both of them are describing the angle type ('c_4', 'c_4', 'h_1').
    LJ126Term('c_4', 'h_1') and MieTerm('c_4', 'h_1') are also duplicated,
    because both of them are describing the vdW interactions between atom types 'c_4' and 'h_1'.

    TODO Because ZFP is designed mainly for FF parameters exchange, several features are not currently supported by ZFP format
    1. Comments for force field and ffterm
    2. Adjustable parameters

    Parameters
    ----------
    file : str

    Attributes
    ----------
    forcefield : ForceField
    '''

    def __init__(self, file):
        self.forcefield = ForceField()
        self._parse(file)

    def _parse(self, file):
        try:
            tree = ET.ElementTree(file=file)
        except:
            raise Exception('Invalid ZFP file')

        root = tree.getroot()
        if root is None:
            raise Exception('Empty ZFP file')

        ff = self.forcefield

        node = root.find('Setting')
        ff.vdw_cutoff = float(node.attrib['vdw_cutoff'])
        ff.vdw_long_range = node.attrib['vdw_long_range']
        ff.lj_mixing_rule = node.attrib['lj_mixing_rule']
        ff.scale_14_vdw = float(node.attrib['scale_14_vdw'])
        ff.scale_14_coulomb = float(node.attrib['scale_14_coulomb'])

        tags = {
            'AtomTypes'           : ff.atom_types,
            'VirtualSiteTerms'    : ff.virtual_site_terms,
            'ChargeIncrementTerms': ff.qinc_terms,
            'VdwTerms'            : ff.vdw_terms,
            'PairwiseVdwTerms'    : ff.pairwise_vdw_terms,
            'BondTerms'           : ff.bond_terms,
            'AngleTerms'          : ff.angle_terms,
            'DihedralTerms'       : ff.dihedral_terms,
            'ImproperTerms'       : ff.improper_terms,
            'PolarizableTerms'    : ff.polarizable_terms,
        }
        _duplicated = []
        for tag, d in tags.items():
            node = root.find(tag)
            if node is None:
                continue
            for element in node:
                try:
                    term = FFTermFactory.create_from_zfp(element.tag, element.attrib)
                except:
                    raise Exception('Invalid tag or attributes: %s, %s' %
                                    (element.tag, str(element.attrib)))
                if term.name in d.keys():
                    _duplicated.append(term)
                else:
                    d[term.name] = term

        if _duplicated:
            msg = f'{len(_duplicated)} duplicated terms from {file}'
            for term in _duplicated:
                msg += f'\n        {term}'
            logger.error(msg)
            raise Exception('Duplicated terms in ZFP file')

    @staticmethod
    def save_to(ff, file):
        '''
        Save ForceField to a ZFP file

        Parameters
        ----------
        ff : ForceField
        file : str
        '''
        root = ET.Element('ForceFieldTerms')

        attrib = {
            'vdw_cutoff'      : str(ff.vdw_cutoff),
            'vdw_long_range'  : ff.vdw_long_range,
            'lj_mixing_rule'  : ff.lj_mixing_rule,
            'scale_14_vdw'    : str(ff.scale_14_vdw),
            'scale_14_coulomb': str(ff.scale_14_coulomb),
        }
        node = ET.SubElement(root, 'Setting', attrib=attrib)

        tags = {
            'AtomTypes'           : ff.atom_types,
            'VirtualSiteTerms'    : ff.virtual_site_terms,
            'ChargeIncrementTerms': ff.qinc_terms,
            'VdwTerms'            : ff.vdw_terms,
            'PairwiseVdwTerms'    : ff.pairwise_vdw_terms,
            'BondTerms'           : ff.bond_terms,
            'AngleTerms'          : ff.angle_terms,
            'DihedralTerms'       : ff.dihedral_terms,
            'ImproperTerms'       : ff.improper_terms,
            'PolarizableTerms'    : ff.polarizable_terms,
        }
        for tag, d in tags.items():
            node = ET.SubElement(root, tag)
            for term in d.values():
                ET.SubElement(node, term.__class__.__name__, attrib=term.to_zfp())

        str_xml = minidom.parseString(ET.tostring(root)).toprettyxml(indent='  ')
        with open(file, 'wb') as f:
            f.write(str_xml.encode())


ForceField.registor_format('.zfp', Zfp)
