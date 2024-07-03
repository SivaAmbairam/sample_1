import csv
import os


def consolidate_matches(input_folder, output_file, supplier_name):
    matched_products = []

    input_folder_path = os.path.abspath(input_folder)
    if not os.path.exists(input_folder_path):
        print(f"Error: The directory {input_folder_path} does not exist.")
        return

    csv_files = [f for f in os.listdir(input_folder_path) if
                 f.endswith('.csv') and f.startswith(f'FlinnVs{supplier_name}')]

    for csv_file in csv_files:
        file_path = os.path.join(input_folder_path, csv_file)
        with open(file_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row[f'{supplier_name}_product_name'] != 'No good match found (Low match score)':
                    match_score = float(row[f'{supplier_name}_Match_Score'])
                    if match_score == 0:
                        keys_to_clear = [
                            f'{supplier_name}_product_category',
                            f'{supplier_name}_product_sub_category',
                            f'{supplier_name}_product_id',
                            f'{supplier_name}_product_name',
                            f'{supplier_name}_product_quantity',
                            f'{supplier_name}_product_price',
                            f'{supplier_name}_product_url',
                            f'{supplier_name}_image_url'
                        ]
                        for key in keys_to_clear:
                            row[key] = ''
                    matched_products.append(row)

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w', newline='') as final_file:
        fieldnames = [
            'Flinn_product_category', 'Flinn_product_sub_category', 'Flinn_product_id',
            'Flinn_product_name', 'Flinn_product_quantity', 'Flinn_product_price',
            'Flinn_product_url', 'Flinn_image_url',
            f'{supplier_name}_product_category', f'{supplier_name}_product_sub_category',
            f'{supplier_name}_product_id', f'{supplier_name}_product_name',
            f'{supplier_name}_product_quantity', f'{supplier_name}_product_price',
            f'{supplier_name}_product_url', f'{supplier_name}_image_url', f'{supplier_name}_Match_Score'
        ]
        writer = csv.DictWriter(final_file, fieldnames=fieldnames)
        writer.writeheader()
        for match in matched_products:
            writer.writerow(match)

    print(f"Final matched products have been saved to {output_file}")


def create_master_csv(suppliers, output_folder, output_file_name):
    master_products = {}

    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, output_file_name)

    for supplier_name in suppliers:
        input_file = os.path.join('Scrapping Scripts', 'Output', 'temp', f'FlinnVs{supplier_name}', 'Matched_Products.csv')
        if not os.path.exists(input_file):
            print(f"Error: The file {input_file} does not exist.")
            continue

        with open(input_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                flinn_product_id = row['Flinn_product_id']
                if flinn_product_id not in master_products:
                    master_products[flinn_product_id] = {
                        'Flinn_product_category': row['Flinn_product_category'],
                        'Flinn_product_sub_category': row['Flinn_product_sub_category'],
                        'Flinn_product_id': row['Flinn_product_id'],
                        'Flinn_product_name': row['Flinn_product_name'],
                        'Flinn_product_quantity': row['Flinn_product_quantity'],
                        'Flinn_product_price': row['Flinn_product_price'],
                        'Flinn_product_url': row['Flinn_product_url'],
                        'Flinn_image_url': row['Flinn_image_url']
                    }
                master_products[flinn_product_id].update({
                    f'{supplier_name}_product_category': row[f'{supplier_name}_product_category'],
                    f'{supplier_name}_product_sub_category': row[f'{supplier_name}_product_sub_category'],
                    f'{supplier_name}_product_id': row[f'{supplier_name}_product_id'],
                    f'{supplier_name}_product_name': row[f'{supplier_name}_product_name'],
                    f'{supplier_name}_product_quantity': row[f'{supplier_name}_product_quantity'],
                    f'{supplier_name}_product_price': row[f'{supplier_name}_product_price'],
                    f'{supplier_name}_product_url': row[f'{supplier_name}_product_url'],
                    f'{supplier_name}_image_url': row[f'{supplier_name}_image_url'],
                    f'{supplier_name}_Match_Score': row[f'{supplier_name}_Match_Score']
                })

    with open(output_file, 'w', newline='') as final_file:
        fieldnames = [
            'Flinn_product_category', 'Flinn_product_sub_category', 'Flinn_product_id',
            'Flinn_product_name', 'Flinn_product_quantity', 'Flinn_product_price',
            'Flinn_product_url', 'Flinn_image_url'
        ]

        if len(suppliers) == 1:
            supplier_name = suppliers[0]
            fieldnames.extend([
                f'{supplier_name}_product_category', f'{supplier_name}_product_sub_category',
                f'{supplier_name}_product_id', f'{supplier_name}_product_name',
                f'{supplier_name}_product_quantity', f'{supplier_name}_product_price',
                f'{supplier_name}_product_url', f'{supplier_name}_image_url',
                f'{supplier_name}_Match_Score'
            ])
        else:
            for supplier_name in suppliers:
                fieldnames.extend([
                    f'{supplier_name}_product_category', f'{supplier_name}_product_sub_category',
                    f'{supplier_name}_product_id', f'{supplier_name}_product_name',
                    f'{supplier_name}_product_quantity', f'{supplier_name}_product_price',
                    f'{supplier_name}_product_url', f'{supplier_name}_image_url',
                    f'{supplier_name}_Match_Score'
                ])

        writer = csv.DictWriter(final_file, fieldnames=fieldnames)
        writer.writeheader()
        for product in master_products.values():
            writer.writerow(product)

    print(f"Master CSV has been saved to {output_file}")


consolidate_matches('Scrapping Scripts/Output/temp/FlinnVsFrey', 'Scrapping Scripts/Output/temp/FlinnVsFrey/Matched_Products.csv', 'Frey')
consolidate_matches('Scrapping Scripts/Output/temp/FlinnVsNasco', 'Scrapping Scripts/Output/temp/FlinnVsNasco/Matched_Products.csv', 'Nasco')
consolidate_matches('Scrapping Scripts/Output/temp/FlinnVsCarolina', 'Scrapping Scripts/Output/temp/FlinnVsCarolina/Matched_Products.csv', 'Carolina')
consolidate_matches('Scrapping Scripts/Output/temp/FlinnVsVWR', 'Scrapping Scripts/Output/temp/FlinnVsVWR/Matched_Products.csv', 'VWR')
consolidate_matches('Scrapping Scripts/Output/temp/FlinnVsFisher', 'Scrapping Scripts/Output/temp/FlinnVsFisher/Matched_Products.csv', 'Fisher')
consolidate_matches('Scrapping Scripts/Output/temp/FlinnVsWardsci', 'Scrapping Scripts/Output/temp/FlinnVsWardsci/Matched_Products.csv', 'Wardsci')


suppliers = ['Frey', 'Nasco', 'Carolina', 'VWR', 'Fisher', 'Wardsci']
create_master_csv(suppliers, 'Scrapping Scripts/Output', 'Master_Matched_Products.csv')


