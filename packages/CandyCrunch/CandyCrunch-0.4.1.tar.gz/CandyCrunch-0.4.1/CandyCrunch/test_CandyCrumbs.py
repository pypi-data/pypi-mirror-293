import unittest
from analysis import CandyCrumbs

class TestCandyCrunch(unittest.TestCase):
    def test_candy_crumbs(self):
        test_dict =   {'glycan_string':"AVAVT*Neu5Ac(a2-3)Gal(a1-3)[Neu5Ac(a2-3)Gal(b1-4)GlcNAc(b1-6)]GalNAc*LQSH",
                        'charge':+2,
                        'label_mass':0,
                        'masses':[156.076, 204.086, 228.09, 243.108, 259.176, 274.092, 292.102, 355.148, 366.14, 425.178, 454.155, 468.232, 564.797, 657.234, 666.339, 747.365, 791.372, 828.393, 860.311, 892.912, 925.51, 973.939, 990.897, 1022.361, 1026.430, 1075.959, 1128.589, 1236.557, 1267.642, 1290.641, 1313.451, 1771.752, 1884.831, 1981.806],
                        'annotations':[[['y_1'],['loss of glycan 1']],[['No_Peptide'],['C_4_Alpha', 'Z_1_Beta', 'Z_1_Alpha']],[['z_2'],['loss of glycan 1']],[['y_2'],['loss of glycan 1']],[['c_3'],['loss of glycan 1']],[['No Peptide'], ['B_1_Beta', 'M_H2O']],[['No Peptide'], ['B_1_Beta']],[['z_3'], ['loss of glycan 1']],[['No Peptide'], ['Y_3_Alpha', 'B_3_Alpha']],[['w_4'], ['loss of glycan 1']],[['No Peptide'], ['B_2_Alpha']],[['z_4'], ['loss of glycan 1']],[['Peptide'], ['Y_1_Beta', 'Y_1_Alpha']],[['No Peptide'], ['B_3_Alpha']],[['Peptide'], ['Y_1_Beta', 'Y_2_Alpha']],[['Peptide'], ['Y_1_Beta', 'Y_3_Alpha']],[['Peptide'], ['Y_1_Alpha']],[['Peptide'], ['Y_2_Beta', 'Y_3_Alpha']],[['No Peptide'], ['Y_1_Beta']],[['Peptide'], ['Y_1_Beta']], [['Peptide'], ['Y_0_Alpha']],[['Peptide'], ['Y_3_Alpha']], [['z_6'], ['M']], [['No Peptide'], ['Y_3_Alpha']], [['z_7'], ['M']], [['z_8'], ['M']], [['Peptide'], ['Y_1_Beta', 'Y_1_Alpha']], [], [], [['Peptide'], ['Y_1_Alpha', 'Y_2_Beta']], [['No Peptide'], ['B_4_Alpha']], [['c_5'], ['M']], [['c_6'], ['M']], [['z_6'], ['M']]],
                        'ref':'https://doi.org/10.1007/s13361-018-1945-7'}
        
        result = CandyCrumbs(test_dict['glycan_string'], test_dict['masses'], 0.2, charge=test_dict['charge'],label_mass=test_dict['label_mass'])
        
        total_annotations = len(test_dict['annotations'])
        correct_annotations = 0
        
        for mass, expected_annotations in zip(test_dict['masses'], test_dict['annotations']):
            if mass in result:
                if result[mass]:
                    predicted_annotations = result[mass]['Domon-Costello nomenclatures'][0]
                    if predicted_annotations == expected_annotations:
                        correct_annotations += 1
                elif not expected_annotations:
                    correct_annotations += 1  # Credit for correctly predicting no annotations
        
        score = correct_annotations / total_annotations if total_annotations > 0 else 1.0
        
        # Set a threshold for acceptable performance (e.g., 80% correct)
        threshold = 0.2
        
        self.assertGreaterEqual(score, threshold, 
                                f"Performance below acceptable threshold. Score: {score:.2f}, Threshold: {threshold}")
        
        print(f"Test passed. Score: {score:.2f}")

if __name__ == '__main__':
    unittest.main()