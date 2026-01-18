import data_loader
import profiler
import reporting

def main():
    try:
        data = data_loader.load_market_data('market_data.csv')
        print(f"Successfully loaded {len(data)} rows.")
    except FileNotFoundError:
        print("market_data.csv not found. Skipping CSV load test.")

    stats = profiler.profile_strategies()
    
    reporting.generate_plots(stats)
    reporting.create_markdown_report(stats)

if __name__ == "__main__":
    main()