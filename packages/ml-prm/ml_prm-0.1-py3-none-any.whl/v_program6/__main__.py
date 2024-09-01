import argparse
from ml_prm import naive_bayes_iris, naive_bayes_newsgroups

def main():
    parser = argparse.ArgumentParser(description='Run Naive Bayes classification.')
    parser.add_argument('dataset', choices=['iris', 'newsgroups'], help='Dataset to use for classification')
    args = parser.parse_args()

    if args.dataset == 'iris':
        accuracy = naive_bayes_iris()
        print(f"Iris dataset accuracy: {accuracy:.2f}")
    elif args.dataset == 'newsgroups':
        accuracy = naive_bayes_newsgroups()
        print(f"Newsgroups dataset accuracy: {accuracy:.2f}")

if __name__ == '__main__':
    main()
