import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
import socket
import sys

def check_internet():
    try:
        # Try to resolve Google's DNS
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def search_book(query, retries=3, delay=5):
    # Encode the search query
    encoded_query = urllib.parse.quote(query)
    
    # Construct the search URL
    search_url = f"https://www.google.com/search?q={encoded_query}"
    
    # Headers to mimic a browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    for attempt in range(retries):
        try:
            # Check internet connection first
            if not check_internet():
                print("No internet connection. Waiting before retry...")
                time.sleep(delay)
                continue

            # Make the request
            response = requests.get(
                search_url, 
                headers=headers, 
                timeout=10,
                verify=True
            )
            response.raise_for_status()
            
            # Parse the HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find the first result link
            search_results = soup.find_all('div', class_='g')
            if search_results:
                first_result = search_results[0]
                link = first_result.find('a')
                if link:
                    return link['href']
            
            return "No link found"

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1}/{retries} failed: {str(e)}")
            if attempt < retries - 1:
                print(f"Waiting {delay} seconds before retrying...")
                time.sleep(delay)
            else:
                return f"Error after {retries} attempts: {str(e)}"
        
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return f"Error: {str(e)}"

def main():
    # List of books to search
    books = [
        "Wings of Fire by Dr. A.P.J. Abdul Kalam in rokomari",
        "Pather Panchali by Bibhutibhushan Bandyopadhyay in rokomari",
        "Feluda Series by Satyajit Ray in rokomari",
        "দুইশো তেরোর গল্প in rokomari",
        "ইন্দুবালা ভাতের হোটেল in rokomari",
        "যদ্যপি আমার গুরু in rokomari",
        "রবীন্দ্রনাথ এখানে কখনও খেতে আসেননি in rokomari",
        "আদর্শ হিন্দু হোটেল in rokomari",
        "Lalsalu by Syed Waliullah in rokomari",
        "The Diary of a Young Girl by Anne Frank in rokomari",
        "Misir Ali Series by Humayun Ahmed in rokomari",
        "Sapiens: A Brief History of Humankind by Yuval Noah Harari in rokomari",
        "Ikigai: The Japanese Secret to a Long and Happy Life by Héctor García in rokomari",
        "The Alchemist by Paulo Coelho in rokomari",
        "1984 by George Orwell in rokomari",
        "Before the Coffee Gets Cold by Toshikazu Kawaguchi in rokomari",
        "টাইম লুপ by খোন্দকার মেহেদী হাসান in rokomari",
        "দ্য হিচহাইকার'স গাইড টু দ্য গ্যালাক্সি by ডগলাস অ্যাডামস্ in rokomari",
        "Cosmos by Carl Sagan in rokomari",
        "The Little Prince by Antoine de Saint-Exupéry in rokomari",
        "The Secret Life of Bees by Sue Monk Kidd in rokomari",
        "Diary of a Wimpy Kid by Jeff Kinney in rokomari",
        "Wonder by R.J. Palacio in rokomari",
        "The Boy in the Striped Pajamas by John Boyne in rokomari",
        "বিজ্ঞানীদের কাণ্ডকারখানা by রাগিব হাসান in rokomari",
        "ভাইরে আপুরে!!! by শাব্বির আহসান in rokomari",
        "লার্নিং হাউ টু ফ্লাই by APJ Abdul Kalam in rokomari"
    ]

    # Check internet connection before starting
    if not check_internet():
        print("No internet connection. Please check your connection and try again.")
        sys.exit(1)

    # Create or open the file in append mode
    with open('book_links.txt', 'w', encoding='utf-8') as f:
        for i, book in enumerate(books, 1):
            print(f"Searching for book {i}/{len(books)}: {book}")
            
            # Search for the book
            link = search_book(book)
            
            # Write to file
            f.write(f"{i}. {book}\n")
            f.write(f"Link: {link}\n\n")
            
            # Rate limiting - wait between requests
            if i < len(books):  # Don't wait after the last book
                wait_time = 3  # 3 seconds between requests
                print(f"Waiting {wait_time} seconds before next search...")
                time.sleep(wait_time)

    print("\nSearch completed. Results saved to book_links.txt")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScript interrupted by user. Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")
        sys.exit(1)