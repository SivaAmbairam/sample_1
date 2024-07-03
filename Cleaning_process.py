import pandas as pd

if __name__ == '__main__':

    demo_df = pd.read_csv('Scrapping Scripts/Output/Product_Comparison_Manual_export.csv', encoding='latin-1')
    flinn_df = pd.read_csv('Scrapping Scripts/Output/Flinn_Products.csv')
    frey_df = pd.read_csv('Scrapping Scripts/Output/Frey_products.csv')
    nasco_df = pd.read_csv('Scrapping Scripts/Output/Nasco_products.csv')
    carolina_df = pd.read_csv('Scrapping Scripts/Output/Carolina_Products.csv')
    vwr_df = pd.read_csv('Scrapping Scripts/Output/VWR_WARDS_Products.csv')
    fisher_df = pd.read_csv('Scrapping Scripts/Output/Fisher_products.csv')
    wardsci_df = pd.read_csv('Scrapping Scripts/Output/Wardsci_products.csv')

    combined_matches = []

    for i, demo_row in demo_df.iterrows():
        demo_flinn_id = demo_row['FLINN_Part_No']
        print(demo_flinn_id)
        demo_frey_id = demo_row['FREY_Part_No']
        demo_nasco_id = demo_row['NASCO_Part_No']
        demo_carolina_id = demo_row['CAROLINA_Part_No']
        demo_vwr_id = demo_row['VWR_WARDS_Part_No']
        demo_fisher_id = demo_row['FISHER_Part_No']
        if 'WARDSCI_Part_No' in str(demo_row):
            demo_wardsci_id = demo_row['WARDSCI_Part_No']
        else:
            demo_wardsci_id = ''
        flinn_match = {}
        frey_match = {}
        nasco_match = {}
        carolina_match = {}
        vwr_match = {}
        fisher_match = {}
        wardsci_match = {}

        if not pd.isna(demo_flinn_id):
            demo_flinn_id = str(demo_flinn_id)
            flinn_match = flinn_df[flinn_df['Flinn_product_id'].astype(str) == demo_flinn_id].drop(columns=['Flinn_product_desc']).to_dict(orient='records')
        if not pd.isna(demo_frey_id):
            demo_frey_id = str(demo_frey_id)
            frey_df['Frey_Match_Score'] = 1
            frey_match = frey_df[frey_df['Frey_product_id'].astype(str) == demo_frey_id].drop(columns=['Frey_product_desc']).to_dict(orient='records')
        if not pd.isna(demo_nasco_id):
            demo_nasco_id = str(demo_nasco_id)
            nasco_df['Nasco_Match_Score'] = 1
            nasco_match = nasco_df[nasco_df['Nasco_product_id'].astype(str) == demo_nasco_id].drop(columns=['Nasco_product_desc']).to_dict(orient='records')
        if not pd.isna(demo_carolina_id):
            demo_carolina_id = str(demo_carolina_id)
            carolina_df['Carolina_Match_Score'] = 1
            carolina_match = carolina_df[carolina_df['Carolina_product_id'].astype(str) == demo_carolina_id].drop(columns=['Carolina_product_desc']).to_dict(orient='records')
        if not pd.isna(demo_vwr_id):
            demo_vwr_id = str(demo_vwr_id)
            vwr_df['VWR_Match_Score'] = 1
            vwr_match = vwr_df[vwr_df['VWR_product_id'].astype(str) == demo_vwr_id].drop(columns=['VWR_product_desc']).to_dict(orient='records')

        if not pd.isna(demo_fisher_id):
            demo_fisher_id = str(demo_fisher_id)
            fisher_df['Fisher_Match_Score'] = 1
            fisher_match = fisher_df[fisher_df['Fisher_product_id'].astype(str) == demo_fisher_id].drop(columns=['Fisher_product_desc']).to_dict(orient='records')

        if not pd.isna(demo_wardsci_id):
            demo_wardsci_id = str(demo_wardsci_id)
            wardsci_df['Wardsci_Match_Score'] = 1
            wardsci_match = wardsci_df[wardsci_df['Wardsci_product_id'].astype(str) == demo_wardsci_id].drop(columns=['Wardsci_product_desc']).to_dict(orient='records')

        if flinn_match:
            best_match_flinn = flinn_match[0]
            if frey_match:
                best_match_frey = frey_match[0]
            else:
                if 'nan' not in str(demo_row['FREY_Description']):
                    frey_match = {
                        'Frey_product_category': '',
                        'Frey_product_sub_category': '',
                        'Frey_product_id': demo_row['FREY_Part_No'],
                        'Frey_product_name': demo_row['FREY_Description'],
                        'Frey_product_quantity': demo_row['FREY_Piece_Count'],
                        'Frey_product_price': '',
                        'Frey_product_url': 'Url not found',
                        'Frey_image_url': '',
                        'Frey_Match_Score': ''
                    }
                else:
                    frey_match = {
                        'Frey_product_category': '',
                        'Frey_product_sub_category': '',
                        'Frey_product_id': '',
                        'Frey_product_name': '',
                        'Frey_product_quantity': '',
                        'Frey_product_price': '',
                        'Frey_product_url': '',
                        'Frey_image_url': '',
                        'Frey_Match_Score': ''
                    }
                best_match_frey = frey_match
            if nasco_match:
                best_match_nasco = nasco_match[0]
            else:
                if 'nan' not in str(demo_row['NASCO_Description']):
                    nasco_match = {
                        'Nasco_product_category': '',
                        'Nasco_product_sub_category': '',
                        'Nasco_product_id': demo_row['NASCO_Part_No'],
                        'Nasco_product_name': demo_row['NASCO_Description'],
                        'Nasco_product_quantity': demo_row['NASCO_Piece_Count'],
                        'Nasco_product_price': '',
                        'Nasco_product_url': 'Url not found',
                        'Nasco_image_url': '',
                        'Nasco_Match_Score': ''
                    }
                else:
                    nasco_match = {
                        'Nasco_product_category': '',
                        'Nasco_product_sub_category': '',
                        'Nasco_product_id': '',
                        'Nasco_product_name': '',
                        'Nasco_product_quantity': '',
                        'Nasco_product_price': '',
                        'Nasco_product_url': '',
                        'Nasco_image_url': '',
                        'Nasco_Match_Score': ''
                    }
                best_match_nasco = nasco_match
            if carolina_match:
                best_match_carolina = carolina_match[0]
            else:
                if 'nan' not in str(demo_row['CAROLINA_Description']):
                    carolina_match = {
                        'Carolina_product_category': '',
                        'Carolina_product_sub_category': '',
                        'Carolina_product_id': demo_row['CAROLINA_Part_No'],
                        'Carolina_product_name': demo_row['CAROLINA_Description'],
                        'Carolina_product_quantity': demo_row['CAROLINA_Piece_Count'],
                        'Carolina_product_price': '',
                        'Carolina_product_url': 'Url not found',
                        'Carolina_image_url': '',
                        'Carolina_Match_Score': ''
                    }
                else:
                    carolina_match = {
                        'Carolina_product_category': '',
                        'Carolina_product_sub_category': '',
                        'Carolina_product_id': '',
                        'Carolina_product_name': '',
                        'Carolina_product_quantity': '',
                        'Carolina_product_price': '',
                        'Carolina_product_url': '',
                        'Carolina_image_url': '',
                        'Carolina_Match_Score': ''
                    }
                best_match_carolina = carolina_match
            if vwr_match:
                best_match_vwr = vwr_match[0]
            else:
                if 'nan' not in str(demo_row['VWR_WARDS_Description']):
                    vwr_match = {
                        'VWR_product_category': '',
                        'VWR_product_sub_category': '',
                        'VWR_product_id': demo_row['VWR_WARDS_Part_No'],
                        'VWR_product_name': demo_row['VWR_WARDS_Description'],
                        'VWR_product_quantity': demo_row['VWR_WARDS_Piece_Count'],
                        'VWR_product_price': '',
                        'VWR_product_url': 'Url not found',
                        'VWR_image_url': '',
                        'VWR_Match_Score': ''
                    }
                else:
                    vwr_match = {
                        'VWR_product_category': '',
                        'VWR_product_sub_category': '',
                        'VWR_product_id': '',
                        'VWR_product_name': '',
                        'VWR_product_quantity': '',
                        'VWR_product_price': '',
                        'VWR_product_url': '',
                        'VWR_image_url': '',
                        'VWR_Match_Score': ''
                    }
                best_match_vwr = vwr_match
            if fisher_match:
                best_match_fisher = fisher_match[0]
            else:
                if 'nan' not in str(demo_row['FISHER_Description']):
                    fisher_match = {
                        'Fisher_product_category': '',
                        'Fisher_product_sub_category': '',
                        'Fisher_product_id': demo_row['FISHER_Part_No'],
                        'Fisher_product_name': demo_row['FISHER_Description'],
                        'Fisher_product_quantity': demo_row['FISHER_Piece_Count'],
                        'Fisher_product_price': '',
                        'Fisher_product_url': 'Url not found',
                        'Fisher_image_url': '',
                        'Fisher_Match_Score': ''
                    }
                else:
                    fisher_match = {
                        'Fisher_product_category': '',
                        'Fisher_product_sub_category': '',
                        'Fisher_product_id': '',
                        'Fisher_product_name': '',
                        'Fisher_product_quantity': '',
                        'Fisher_product_price': '',
                        'Fisher_product_url': '',
                        'Fisher_image_url': '',
                        'Fisher_Match_Score': ''
                    }
                best_match_fisher = fisher_match
            if wardsci_match:
                best_match_wardsci = wardsci_match[0]
            else:
                if 'WARDSCI_Description' in str(demo_row):
                    if 'nan' not in str(demo_row['WARDSCI_Description']):
                        wardsci_match = {
                            'Wardsci_product_category': '',
                            'Wardsci_product_sub_category': '',
                            'Wardsci_product_id': demo_row['WARDSCI_Part_No'],
                            'Wardsci_product_name': demo_row['WARDSCI_Description'],
                            'Wardsci_product_quantity': demo_row['WARDSCI_Piece_Count'],
                            'Wardsci_product_price': '',
                            'Wardsci_product_url': 'Url not found',
                            'Wardsci_image_url': '',
                            'Wardsci_Match_Score': ''
                        }
                    else:
                        wardsci_match = {
                            'Wardsci_product_category': '',
                            'Wardsci_product_sub_category': '',
                            'Wardsci_product_id': '',
                            'Wardsci_product_name': '',
                            'Wardsci_product_quantity': '',
                            'Wardsci_product_price': '',
                            'Wardsci_product_url': '',
                            'Wardsci_image_url': '',
                            'Wardsci_Match_Score': ''
                        }
                    best_match_wardsci = wardsci_match
                else:
                    wardsci_match = {
                        'Wardsci_product_category': '',
                        'Wardsci_product_sub_category': '',
                        'Wardsci_product_id': '',
                        'Wardsci_product_name': '',
                        'Wardsci_product_quantity': '',
                        'Wardsci_product_price': '',
                        'Wardsci_product_url': '',
                        'Wardsci_image_url': '',
                        'Wardsci_Match_Score': ''
                    }
                best_match_wardsci = wardsci_match
            combined_match = {**best_match_flinn, **best_match_frey, **best_match_nasco, **best_match_carolina, **best_match_vwr, **best_match_fisher, **best_match_wardsci}
            combined_matches.append(combined_match)
    combined_df = pd.DataFrame(combined_matches)
    combined_df.to_csv('Scrapping Scripts/Output/Master_file.csv', index=False)