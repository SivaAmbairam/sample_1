import pandas as pd

if __name__ == '__main__':
    master_df = pd.read_csv('Scrapping Scripts/Output/Master_file.csv')
    other_matched_df = pd.read_csv('Scrapping Scripts/Output/Master_Matched_Products.csv')
    updated_rows = []
    for i, master_row in master_df.iterrows():
        master_id = master_row['Flinn_product_id']
        if master_id in other_matched_df['Flinn_product_id'].values:
            matched_row = other_matched_df[other_matched_df['Flinn_product_id'] == master_id].iloc[0]
            updated_row = master_row.to_dict()
            if 'Url not found' in str(master_row['Frey_product_url']) or 'nan' in str(master_row['Frey_product_name']):
                updated_row.update({
                    'Frey_product_category': matched_row['Frey_product_category'],
                    'Frey_product_sub_category': matched_row['Frey_product_sub_category'],
                    'Frey_product_id': matched_row['Frey_product_id'],
                    'Frey_product_name': matched_row['Frey_product_name'],
                    'Frey_product_quantity': matched_row['Frey_product_quantity'],
                    'Frey_product_price': matched_row['Frey_product_price'],
                    'Frey_product_url': matched_row['Frey_product_url'],
                    'Frey_image_url': matched_row['Frey_image_url'],
                    'Frey_Match_Score': matched_row['Frey_Match_Score']
                })

            if 'Url not found' in str(master_row['Nasco_product_url']) or 'nan' in str(master_row['Nasco_product_name']):
                updated_row.update({
                    'Nasco_product_category': matched_row['Nasco_product_category'],
                    'Nasco_product_sub_category': matched_row['Nasco_product_sub_category'],
                    'Nasco_product_id': matched_row['Nasco_product_id'],
                    'Nasco_product_name': matched_row['Nasco_product_name'],
                    'Nasco_product_quantity': matched_row['Nasco_product_quantity'],
                    'Nasco_product_price': matched_row['Nasco_product_price'],
                    'Nasco_product_url': matched_row['Nasco_product_url'],
                    'Nasco_image_url': matched_row['Nasco_image_url'],
                    'Nasco_Match_Score': matched_row['Nasco_Match_Score']
                })

            if 'Url not found' in str(master_row['Carolina_product_url']) or 'nan' in str(master_row['Carolina_product_name']):
                updated_row.update({
                    'Carolina_product_category': matched_row['Carolina_product_category'],
                    'Carolina_product_sub_category': matched_row['Carolina_product_sub_category'],
                    'Carolina_product_id': matched_row['Carolina_product_id'],
                    'Carolina_product_name': matched_row['Carolina_product_name'],
                    'Carolina_product_quantity': matched_row['Carolina_product_quantity'],
                    'Carolina_product_price': matched_row['Carolina_product_price'],
                    'Carolina_product_url': matched_row['Carolina_product_url'],
                    'Carolina_image_url': matched_row['Carolina_image_url'],
                    'Carolina_Match_Score': matched_row['Carolina_Match_Score']
                })

            if 'Url not found' in str(master_row['VWR_product_url']) or 'nan' in str(master_row['VWR_product_name']):
                updated_row.update({
                    'VWR_product_category': matched_row['VWR_product_category'],
                    'VWR_product_sub_category': matched_row['VWR_product_sub_category'],
                    'VWR_product_id': matched_row['VWR_product_id'],
                    'VWR_product_name': matched_row['VWR_product_name'],
                    'VWR_product_quantity': matched_row['VWR_product_quantity'],
                    'VWR_product_price': matched_row['VWR_product_price'],
                    'VWR_product_url': matched_row['VWR_product_url'],
                    'VWR_image_url': matched_row['VWR_image_url'],
                    'VWR_Match_Score': matched_row['VWR_Match_Score']
                })
            if 'Url not found' in str(master_row['Fisher_product_url']) or 'nan' in str(master_row['Fisher_product_name']):
                updated_row.update({
                    'Fisher_product_category': matched_row['Fisher_product_category'],
                    'Fisher_product_sub_category': matched_row['Fisher_product_sub_category'],
                    'Fisher_product_id': matched_row['Fisher_product_id'],
                    'Fisher_product_name': matched_row['Fisher_product_name'],
                    'Fisher_product_quantity': matched_row['Fisher_product_quantity'],
                    'Fisher_product_price': matched_row['Fisher_product_price'],
                    'Fisher_product_url': matched_row['Fisher_product_url'],
                    'Fisher_image_url': matched_row['Fisher_image_url'],
                    'Fisher_Match_Score': matched_row['Fisher_Match_Score']
                })
            if 'Url not found' in str(master_row['Wardsci_product_url']) or 'nan' in str(master_row['Wardsci_product_name']):
                updated_row.update({
                    'Wardsci_product_category': matched_row['Wardsci_product_category'],
                    'Wardsci_product_sub_category': matched_row['Wardsci_product_sub_category'],
                    'Wardsci_product_id': matched_row['Wardsci_product_id'],
                    'Wardsci_product_name': matched_row['Wardsci_product_name'],
                    'Wardsci_product_quantity': matched_row['Wardsci_product_quantity'],
                    'Wardsci_product_price': matched_row['Wardsci_product_price'],
                    'Wardsci_product_url': matched_row['Wardsci_product_url'],
                    'Wardsci_image_url': matched_row['Wardsci_image_url'],
                    'Wardsci_Match_Score': matched_row['Wardsci_Match_Score']
                })
            updated_rows.append(updated_row)
        else:
            updated_rows.append(master_row.to_dict())

    unmatched_rows = other_matched_df[~other_matched_df['Flinn_product_id'].isin(master_df['Flinn_product_id'])]
    updated_rows.extend(unmatched_rows.to_dict(orient='records'))
    updated_master_df = pd.DataFrame(updated_rows)
    updated_master_df.to_csv('Scrapping Scripts/Output/Updated_Master_file.csv', index=False)



