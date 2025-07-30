import requests
import json

def get_word_definition(word):
    """
    Get word definition from free dictionary API
    """
    try:
        # Clean the word
        word = word.strip().lower()
        
        # Use free dictionary API
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data and len(data) > 0:
                entry = data[0]
                word_text = entry.get('word', word).title()
                
                # Get pronunciation if available
                phonetics = entry.get('phonetics', [])
                pronunciation = ""
                for phonetic in phonetics:
                    if phonetic.get('text'):
                        pronunciation = f" /{phonetic['text']}/"
                        break
                
                # Get meanings
                meanings = entry.get('meanings', [])
                if meanings:
                    result = f"📖 **{word_text}**{pronunciation}\n\n"
                    
                    for i, meaning in enumerate(meanings[:2]):  # Limit to 2 meanings
                        part_of_speech = meaning.get('partOfSpeech', '').title()
                        definitions = meaning.get('definitions', [])
                        
                        if definitions:
                            result += f"**{part_of_speech}:**\n"
                            
                            # Add up to 2 definitions per part of speech
                            for j, definition in enumerate(definitions[:2]):
                                def_text = definition.get('definition', '')
                                example = definition.get('example', '')
                                
                                result += f"{j+1}. {def_text}\n"
                                if example:
                                    result += f"   📝 *Example: {example}*\n"
                            
                            result += "\n"
                    
                    return result.strip()
                
        elif response.status_code == 404:
            return f"❌ Sorry, I couldn't find the definition for '{word}'. Please check the spelling and try again."
        
        else:
            return f"❌ Error looking up '{word}'. Please try again later."
            
    except requests.exceptions.Timeout:
        return "⏱️ The dictionary service is taking too long to respond. Please try again."
    
    except requests.exceptions.ConnectionError:
        return "🌐 Unable to connect to dictionary service. Please check your internet connection."
    
    except Exception as e:
        return f"❌ An error occurred while looking up '{word}'. Please try again."

def is_dictionary_request(message):
    """
    Check if message is asking for word definition
    """
    message = message.lower().strip()
    
    # Common patterns for dictionary requests
    patterns = [
        "define ",
        "definition of ",
        "meaning of ",
        "what is ",
        "what does ",
        "dictionary ",
    ]
    
    for pattern in patterns:
        if message.startswith(pattern):
            return True
    
    # Check for "define:" format
    if "define:" in message:
        return True
    
    return False

def extract_word_from_message(message):
    """
    Extract the word to define from the message
    """
    message = message.lower().strip()
    
    # Remove common prefixes
    prefixes = [
        "define ",
        "definition of ",
        "meaning of ",
        "what is ",
        "what does ",
        "dictionary ",
        "define:",
    ]
    
    for prefix in prefixes:
        if message.startswith(prefix):
            word = message[len(prefix):].strip()
            # Remove common suffixes
            suffixes = [" mean", " means", "?"]
            for suffix in suffixes:
                if word.endswith(suffix):
                    word = word[:-len(suffix)].strip()
            return word
    
    # Handle "define:" format
    if "define:" in message:
        word = message.split("define:")[1].strip()
        return word
    
    return message.strip()

# Test function
if __name__ == "__main__":
    # Test the dictionary function
    test_words = ["hello", "python", "artificial", "invalid_word_xyz"]
    
    for word in test_words:
        print(f"\n🧪 Testing: {word}")
        print("-" * 40)
        result = get_word_definition(word)
        print(result)
        print("-" * 40)
