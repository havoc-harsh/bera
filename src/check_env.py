import os

def check_environment():
    """Check if all required environment variables are set."""
    required_vars = ['PINECONE_API_KEY', 'GEMINI_API_KEY']
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"ERROR: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these variables in your environment or .env file.")
        return False
    
    print("All required environment variables are set.")
    return True

if __name__ == "__main__":
    check_environment() 