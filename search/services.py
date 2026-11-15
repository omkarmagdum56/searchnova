import requests

def search_duckduckgo(query):
    """DuckDuckGo API वरून जास्तीत जास्त रिझल्ट्स आणणारे फंक्शन"""
    items = []
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
    
    try:
        response = requests.get(url, timeout=5)
        data = response.json()
        
        # १. मुख्य Abstract (जर असेल तर)
        if data.get('AbstractText'):
            items.append({
                'title': data.get('Heading', query),
                'url': data.get('AbstractURL', '#'),
                'description': data.get('AbstractText'),
                'source': 'Live Web Summary'
            })
            
        # २. RelatedTopics मधून रिझल्ट्स गोळा करणे
        for topic in data.get('RelatedTopics', []):
            # काहीवेळा RelatedTopics च्या आतमध्ये पण 'Topics' असतात (Nested structure)
            if 'Topics' in topic:
                for sub_topic in topic['Topics']:
                    if 'Text' in sub_topic and 'FirstURL' in sub_topic:
                        items.append({
                            'title': sub_topic['Text'].split(' - ')[0] if ' - ' in sub_topic['Text'] else sub_topic['Text'][:60],
                            'url': sub_topic['FirstURL'],
                            'description': sub_topic['Text'],
                            'source': 'Live Web (DuckDuckGo)'
                        })
            elif 'Text' in topic and 'FirstURL' in topic:
                items.append({
                    'title': topic['Text'].split(' - ')[0] if ' - ' in topic['Text'] else topic['Text'][:60],
                    'url': topic['FirstURL'],
                    'description': topic['Text'],
                    'source': 'Live Web (DuckDuckGo)'
                })
                
        # ३. जर तरीही रिझल्ट्स कमी पडत असतील, तर Result (Results list) मधून घेणे
        for res in data.get('Results', []):
            if 'Text' in res and 'FirstURL' in res:
                items.append({
                    'title': res['Text'][:60],
                    'url': res['FirstURL'],
                    'description': res['Text'],
                    'source': 'Live Web (DuckDuckGo)'
                })

    except Exception as e:
        print("DuckDuckGo API Error:", e)

    return items