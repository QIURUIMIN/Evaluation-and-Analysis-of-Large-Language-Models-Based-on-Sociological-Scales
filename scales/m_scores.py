import pandas as pd

def calculate_personality_scores(file_path):
    # Load the Excel file
    data = pd.read_excel(file_path)

    # Define the indices for each personality dimension
    e_indices = [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44]
    s_indices = [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45]
    t_indices = [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46]
    j_indices = [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47]

    # Calculate sums for each personality dimension
    results = {
        "E": data.iloc[e_indices]['Value A'].sum(),
        "I": data.iloc[e_indices]['Value B'].sum(),
        "S": data.iloc[s_indices]['Value A'].sum(),
        "N": data.iloc[s_indices]['Value B'].sum(),
        "T": data.iloc[t_indices]['Value A'].sum(),
        "F": data.iloc[t_indices]['Value B'].sum(),
        "J": data.iloc[j_indices]['Value A'].sum(),
        "P": data.iloc[j_indices]['Value B'].sum()
    }

    # Determine the personality type
    personality_type = []
    personality_type.append('E' if results['E'] >= results['I'] else 'I')
    personality_type.append('S' if results['S'] >= results['N'] else 'N')
    personality_type.append('T' if results['T'] >= results['F'] else 'F')
    personality_type.append('J' if results['J'] >= results['P'] else 'P')
    personality_type = ''.join(personality_type)  # Join the letters

    # Add personality type to the results dictionary
    results['Personality Type'] = personality_type

    # Create a DataFrame from the results
    results_df = pd.DataFrame([results])

    # Save the results to a new Excel file
    output_path = file_path.replace('.xlsx', '_Personality_Scores.xlsx')
    results_df.to_excel(output_path, index=False)

    return output_path, personality_type

# Example usage
file_path = 'ENTJ_Extracted_Values.xlsx'
output_file, personality_type = calculate_personality_scores(file_path)
print(f'Personality scores and type {personality_type} saved to {output_file}')

