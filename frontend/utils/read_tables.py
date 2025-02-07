import pandas as pd
import pdfplumber


def extract_table(input_pdfs):
    for input_pdf in input_pdfs:
    
        table_name = input_pdf.split('_')[-1].split('.')[0]
        # Creare una lista temporanea per memorizzare le tabelle di ogni PDF
        tables_in_pdf = []
        print(f"Storing: ",table_name)

        with pdfplumber.open(input_pdf) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                # Estrai tutte le tabelle della pagina
                tables = page.extract_tables()
                for table in tables:
                    df = pd.DataFrame(table)
                    tables_in_pdf.append(df)

        # Concatena tutte le tabelle di un singolo PDF in un unico DataFrame
        if tables_in_pdf:
            combined_pdf_df = pd.concat(tables_in_pdf, ignore_index=True)
    
        combined_pdf_df.to_csv(f"{table_name}.csv", index=False)