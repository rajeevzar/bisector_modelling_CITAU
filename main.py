# main.py

from src.bisector_model import BisectorModel

if __name__ == "__main__":
    # Initialize the model with the input data file and output directory
    model = BisectorModel(data_file="data/CITAU_Bis_ccf_Eder_All_15.txt", output_dir="output/")
    
    # Load the bisector data
    model.load_data()
    
    # Run the simulation with a specified number of iterations
    model.run_simulation(iterations=100)
