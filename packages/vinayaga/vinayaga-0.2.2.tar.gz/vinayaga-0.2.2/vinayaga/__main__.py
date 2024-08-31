# vinayaga/__main__.py

from vinayaga import load_data, train

def main():
    # Load the data from the CSV file
    attributes, target = load_data('data.csv')
    
    print("\nThe attributes are:", attributes)
    print("\nThe target is:", target)
    
    # Train the model to find the specific hypothesis
    final_hypothesis = train(attributes, target)
    
    print("\nThe final hypothesis is:", final_hypothesis)

if __name__ == "__main__":
    main()
