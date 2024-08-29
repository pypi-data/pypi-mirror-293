# Define the DataFrame globally within the module
df = None

def set_df(dataframe):
    global df
    df = dataframe

## _____________________________________________________________________ Function to filter and list cases

# Function to filter and list cases
def FLT_LIST(COND=None, LIST=[]):

    """
    Function to filter and list cases based on a condition.
    
    Parameters:
    COND : boolean Series
        Condition to filter the DataFrame.
    LIST : list of str
        List of columns to display in the filtered output.
    """

    global df
    num_cases_read = df.shape[0]
    filtered_df = df[COND]
    num_cases_listed = filtered_df.shape[0]
    if num_cases_listed > 0:
      print(filtered_df[LIST].reset_index(drop=True).to_string(index=False))
    print(f"\nNumber of cases read:  {num_cases_listed}    Number of cases listed:  {num_cases_listed}\n\n")

#### Example
#### FLT_LIST(COND=df['CID'].isna() | (df['CID']<=0), LIST=['CID', 'CID'])

##______________________________________________________________________________________ SR function.

# General function to process SR filter variables
def SR(Rout='QFILTER', QVAR=[], RNG=[], LIST=[]):

    """
    Function to process Single Response variables.
    
    Parameters:
    Rout : str
        Column name for the filter variable.
    QVAR : str
        Column name for the question variable.
    RNG : list of int
        List of valid range values for the question variable.
    LIST : list of str
        List of columns to display in the filtered output.
    """

    global df    
    # Define the condition for filtering
    condition_qfilter1 = (df[Rout] == 1) & (df[QVAR].isna() | ~df[QVAR].isin(RNG))
    condition_qfilter0 = (df[Rout] != 1) & ~df[QVAR].isna()
    condition = condition_qfilter1 | condition_qfilter0

    # Filter and list based on the condition
    FLT_LIST(condition, [df.columns[0],QVAR]+LIST)

    # Clean up
    df.drop(columns=[Rout], inplace=True)

#### Example for filter question
#### df['QFILTER'] = 0
#### df.loc[df['Q30'].between(2,5), 'QFILTER'] = 1
### SR(Rout='QFILTER', QVAR='Q30a', RNG=list(range(1,17)) + [97],LIST=['CID','Q30a','Q30'])

#### Example for Ask all question
#### df['QFILTER'] = 1
#### SR(Rout='QFILTER',QVAR='Q1', RNG=list(range(3,9)), LIST=['CID','Q1'])

#_____________________________________________________________________ MULTI function

# Define the MULTI function
def MULTI(Rout='QFILTER', QVAR=[], QEX=[],LIST=[]):

    """
    Function to process Multi question variables with exclusive checks.
    
    Parameters:
    Rout : str
        Column name for the filter variable.
    QVAR : list of str
        List of question variable column names.
    QEX : list of str
        List of exclusive variable column names.
    LIST : list of str
        List of columns to display in the filtered output.
    """

    global df    
    NR=len(QVAR)+len(QEX)
    # Calculate QCount1 and QCount2
    df['QCount1'] = df[QVAR + QEX].apply(lambda x: (x == 1).sum(), axis=1)
    df['QCount2'] = df[QVAR + QEX].apply(lambda x: x.isin([0, 1]).sum(), axis=1)

    # Nothing Selected
    print(f"{QVAR[0]} - Nothing Selected:")
    condition1 = (df['QCount1'] == 0) & (df[Rout] == 1)
    FLT_LIST(condition1, [df.columns[0], Rout] + QVAR + QEX+LIST)

    # Invalid Punches
    print(f"{QVAR[0]} - Invalid Punches:")
    condition2 = (df['QCount2'] != NR) & (df[Rout] == 1)
    FLT_LIST(condition2, [df.columns[0], Rout] + QVAR + QEX+LIST)

    # Calculate QCount3
    df['QCount3'] = df[QEX].apply(lambda x: (x == 1).sum(), axis=1)

    # Exclusive Check
    if len(QEX)!=0:
      print(f"{QVAR[0]} - Exclusive Check:")
      condition3 = ((df['QCount1'] > 1) & (df['QCount3'] == 1)) | (df['QCount3'] > 1)
      FLT_LIST(condition3, [df.columns[0], Rout] + QVAR + QEX+LIST)

    # Filter OFF Check
    if ((df[Rout] == 0).sum(axis=0)>0):
      print(f"{QVAR[0]} - Filter OFF Check:")
      condition4 = (df[QVAR + QEX].isna().sum(axis=1) != NR) & ((df[Rout] == 0) | (df[Rout].isna()))
      FLT_LIST(condition4, [df.columns[0], Rout] + QVAR + QEX+LIST)

    # Clean up temporary columns
    NR=0
    df.drop(columns=['QCount1', 'QCount2', 'QCount3', Rout], inplace=True)

#### Example
#### df['QFILTER'] = 0
#### df.loc[df['Q28'].between(2,5), 'QFILTER'] = 1
#### MULTI(Rout='QFILTER', QVAR=['Q29_1', 'Q29_2','Q29_3'], EX=['Q29_99'], NR=4)

#_____________________________________________________________________ GRID function

# Combined function to process grid questions and filter checks
def GRID_CHECK(Rout='QFILTER', QVAR=[], CVAR=[], COD=[], LIST=[]):

    """
    Function to process grid questions with specific codes and filter checks.
    
    Parameters:
    Rout : str
        Column name for the filter variable.
    QVAR : list of str
        List of question variable column names.
    COD : list of int
        List of valid codes for the question variables.
    LIST : list of str
        List of columns to display in the filtered output.
    """

    global df    
    NR=len(QVAR)
    # Handle GRID functionality if Rout is provided
    if len(CVAR)==0:
        #Count the occurrences of COD in QVAR columns
        df['QCount1'] = df[QVAR].apply(lambda x: x.isin(COD).sum(), axis=1)

        # Step 1: Invalid Punches
        print(f"{QVAR[0]} - Invalid Punches:")
        condition1 = (df[Rout] == 1) & (df['QCount1'] != NR)
        FLT_LIST(COND=condition1, LIST=[df.columns[0], Rout] + QVAR)

        # Step 2: Filter OFF Check
        if ((df[Rout] == 0).sum(axis=0)>0):
           print(f"{QVAR[0]} - Filter OFF Check:")
           condition2 = ((df[Rout] == 0) | df[Rout].isna()) & (df[QVAR].isna().sum(axis=1) != NR)
           FLT_LIST(COND=condition2, LIST=[df.columns[0], Rout] + QVAR + LIST)

        # Clean up temporary columns
        NR=0
        df.drop(columns=['QCount1'], inplace=True)

    # Handle GRID_FLT functionality if CVAR is provided
    if len(CVAR)!=0:
        df['err'] = 0
        for i, (x_col, d_col) in enumerate(zip(QVAR, CVAR), start=1):
            df.loc[(df[d_col] == 1) & (df[x_col].isna() | ~df[x_col].isin(COD)), 'err'] = i
            df.loc[(df[d_col] != 1) & df[x_col].notna(), 'err'] = i + 100
        FLT_LIST(COND=(df['err'] > 0), LIST=[df.columns[0], 'err'] + CVAR + QVAR+LIST)

        # Clean up temporary columns
        NR=0
        df.drop(columns=['err',Rout], inplace=True)

# Perform the GRID check
## GRID_CHECK(Rout='QFILTER', QVAR=['Q56_1', 'Q56_2'], COD=[1, 2, 3, 4, 5], LIST=[])

# Perform the GRID_FLT check
## GRID_CHECK(QVAR=['QCN5e_1', 'QCN5e_2', 'QCN5e_3', 'QCN5e_4', 'QCN5e_5'], CVAR=['QCN5d_1', 'QCN5d_2', 'QCN5d_3', 'QCN5d_4', 'QCN5d_5'], COD=[1, 2, 3, 4, 5], LIST=[])

#_____________________________________________________________________ RANK function


def RANK_CHECK(Rout='QFILTER', QVAR=[], MAXR=0, MINR=None):
    """
    Function to process rank order questions with specific checks:
    1. Minimum Rank Check (if MINR is specified)
    2. Invalid Punches
    3. Duplicate Ranks
    4. Filter OFF Check

    Parameters:
    Rout : str
        Column name for the routing/filter variable.
    QVAR : list of str
        List of rank order question columns.
    MAXR : int
        Maximum rank value.
    MINR : int or None
        Minimum rank value (optional, used for rank varying).
    """

    global df    
    NR=len(QVAR)
    # Count the number of valid ranks (1 thru MAXR) for each respondent
    df['QCount1'] = df[QVAR].apply(lambda x: x.between(1, MAXR).sum(), axis=1)

    if MINR is not None:
        # Find the maximum rank value for each respondent
        df['QMAXR'] = df[QVAR].max(axis=1)

        # 1. Minimum Rank Check
        print(f"{QVAR[0]} - Minimum Rank Check:")
        condition_min_rank = (df[Rout] == 1) & (df['QMAXR'] < MINR)
        FLT_LIST(COND=condition_min_rank, LIST=[df.columns[0], Rout, 'QCount1'] + QVAR)

    # 2. Invalid Punches
    print(f"{QVAR[0]} - Invalid Punches:")
    if MINR is not None:
        condition_invalid = (df[Rout] == 1) & ((df[QVAR].isna().sum(axis=1) != (NR - df['QCount1'])) | (df['QCount1'] == 0))
    else:
        condition_invalid = (df[Rout] == 1) & ((df['QCount1'] != MAXR) | (df[QVAR].isna().sum(axis=1) != (NR - MAXR)))
    FLT_LIST(COND=condition_invalid, LIST=[df.columns[0], Rout, 'QCount1'] + QVAR)

    # 3. Duplicate Ranks
    print(f"{QVAR[0]} - Duplicate Ranks:")
    df['err'] = 0
    for i in range(1, MAXR + 1):
        df['cnt'] = df[QVAR].apply(lambda x: (x == i).sum(), axis=1)
        if MINR is not None:
            df.loc[(df[Rout] == 1) & (i <= df['QCount1']) & (df['cnt'] != 1), 'err'] = i
        else:
            df.loc[(df[Rout] == 1) & (df['cnt'] != 1), 'err'] = i
    condition_duplicate = df['err'] != 0
    FLT_LIST(COND=condition_duplicate, LIST=[df.columns[0], Rout, 'QCount1'] + QVAR)

    # 4. Filter OFF Check
    if ((df[Rout] == 0).sum(axis=0)>0):
        print(f"{QVAR[0]} - Filter OFF Check:")
        condition_filter_off = ((df[Rout] == 0) | (df[Rout].isna())) & (df[QVAR].isna().sum(axis=1) != NR)
        FLT_LIST(COND=condition_filter_off, LIST=[df.columns[0], Rout] + QVAR)

    # Clean up temporary columns
    cols_to_drop = ['QCount1', 'err', 'cnt']
    if MINR is not None:
        cols_to_drop.append('QMAXR')
    df.drop(columns=cols_to_drop, inplace=True)

# Example usage for varying rank (RANK_VARY):
# Assuming 'Routing' is the routing variable, and the rank order questions are in columns Q180_Orderr1 to Q180_Orderr5
# RANK_CHECK(Rout='Routing', QVAR=['Q180_Orderr1', 'Q180_Orderr2', 'Q180_Orderr3', 'Q180_Orderr4', 'Q180_Orderr5'], MINR=1, MAXR=3)

# Example usage for fixed rank (RANK_FIXED):
# Assuming 'Routing' is the routing variable, and the rank order questions are in columns Q180_Orderr1 to Q180_Orderr5
# RANK_CHECK(Rout='Routing', QVAR=['Q180_Orderr1', 'Q180_Orderr2', 'Q180_Orderr3', 'Q180_Orderr4', 'Q180_Orderr5'], MAXR=5)









