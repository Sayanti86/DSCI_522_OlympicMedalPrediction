
# coding: utf-8
# 3_DecissionTree.py
#
# This script reads wrangled data and fits DecissionTreeRegressor model to predict the
# Olympic Medal count for 2020 Summer for each country.It splits the data into 80-20 division
# This has three targets (count of gold , count of silver , count of bronze)
# The prediction is done on each target and final report has been prepared with all three
# count predictions of medals .
# The model uses Features : home_adv,population,GDP_USD,last_medals,secondLast_medals
# Target : tot_gold,tot_silver,tot_bronze
# Dependencies: argparse, pandas, numpy , sklearn
#
# Usage: python src/3_DecissionTree.py results/clean_medal_count_data.csv results/prediction_output.csv

# import libraries
import argparse
import pandas as pd
import numpy as np
from sklearn import tree
from sklearn.model_selection import train_test_split

# read in command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('input_file')
parser.add_argument('out_file')
args = parser.parse_args()

def main():
    # Read input file.
    clean_data = pd.read_csv(args.input_file)

    # Building Features for final test split :
    clean_data_2020 = pd.read_csv("results/tokyo_2020_test_data.csv")
    feature_cols = ['home_adv','last_medals','secondLast_medals','population','GDP_USD']
    finaltest = clean_data_2020.loc[:, feature_cols]

    # Building Features for train and validation splits.
    feature_cols1 = ['home_adv','last_medals','secondLast_medals','population','GDP_USD']

    X = clean_data.loc[:, feature_cols1]
    #Setting three different medals(gold , silver ,bronze) as target.
    g = clean_data.tot_gold
    s = clean_data.tot_silver
    b = clean_data.tot_bronze

    # shuffles and then splits .
    Xtrain, Xtest, gtrain, gtest,strain,stest,btrain,btest = train_test_split(X,g,s,b,test_size=0.2)

    #Model DecisionTreeClassifier() as our target is string.
    model = tree.DecisionTreeRegressor()

    # GOLD : Model fit , Predict,score , final output predit column.
    model.fit(Xtrain, gtrain)
    predict= model.predict(Xtest)
    #print("TestScore of Gold",model.score(Xtest, gtest))
    # Getting the prediction of gold on full data .
    #This will be used to build the final output file.
    predictions_gold = model.predict(finaltest)

    # SILVER : Model fit , Predict,score , final output predit column.
    model.fit(Xtrain, strain)
    predict= model.predict(Xtest)
    #print("TestScore of Silver",model.score(Xtest, stest))
    # Getting the prediction of silver on full data .
    #This will be used to build the final output file.
    predictions_silver = model.predict(finaltest)

    # BRONZE : Model fit , Predict,score , final output predit column.
    model.fit(Xtrain, btrain)
    predict= model.predict(Xtest)
    #print("TestScore of Bronze",model.score(Xtest, btest))
    # Getting the prediction of bronze on full data .
    #This will be used to build the final output file.
    predictions_bronze = model.predict(finaltest)

    # Final output file preparation with all three medal count prediction.
    pred_dict = clean_data_2020.copy()
    pred_dict['predictions_gold'] = predictions_gold
    pred_dict['predictions_silver'] = predictions_silver
    pred_dict['predictions_bronze'] = predictions_bronze
    pd.DataFrame(pred_dict)

    #Write csv of final data.
    pred_dict.to_csv(args.out_file)

# call main function
if __name__ == "__main__":
    main()
