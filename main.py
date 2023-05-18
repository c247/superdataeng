import pandas as pd
import re
from io import StringIO
from tabulate import tabulate

def clean_airline_code(airline_code):
    cleaned_code = re.sub(r'[^\w\s]', '', airline_code)
    cleaned_code = cleaned_code.strip()
    return cleaned_code

def process_data(input_data):
    # Transfer input into pandas dataframe
    data_frame = pd.read_csv(StringIO(input_data), sep=';')

    # Step 1. Add the missing flight codes and convert to int
    data_frame['FlightCodes'] = pd.to_numeric(data_frame['FlightCodes'], errors='coerce')
    data_frame['FlightCodes'] = data_frame['FlightCodes'].interpolate(method='linear', limit_direction='forward', downcast='infer', step=10)
    data_frame['FlightCodes'] = data_frame['FlightCodes'].astype(int)

    # Step 2. Split To_From into To and From columns and capitalize values
    data_frame[['To', 'From']] = data_frame['To_From'].str.split('_', expand=True)
    data_frame['To'] = data_frame['To'].str.upper()
    data_frame['From'] = data_frame['From'].str.upper()
    data_frame = data_frame.drop('To_From', axis=1)  # Remove old column

    # Step 3. Remove punctuation from airline code and leading/trailing whitespace
    data_frame['Airline Code'] = data_frame['Airline Code'].apply(clean_airline_code)

    return data_frame

def format_dataframe(data_frame):
    table = tabulate(data_frame, headers='keys', tablefmt='psql')
    print(table)

def format_dataframe_stringified(data_frame):
    transformed_table = processed_data.to_csv(index=False, sep=';', line_terminator='\n')
    table = transformed_table.replace("\n", "\\n")
    print(table)


# Input table
input_data = 'Airline Code;DelayTimes;FlightCodes;To_From\nAir Canada (!);[21, 40];20015.0;WAterLoo_NEWYork\n<Air France> (12);[];;Montreal_TORONTO\n(Porter Airways. );[60, 22, 87];20035.0;CALgary_Ottawa\n12. Air France;[78, 66];;Ottawa_VANcouvER\n""".\\.Lufthansa.\\.""";[12, 33];20055.0;london_MONTreal\n'

# Transform table
processed_data = process_data(input_data)

# Print the resulting transformed table
format_dataframe(processed_data)
format_dataframe_stringified(processed_data)
