# Reflection

Student Name:  Solomon Burt
Sudent Email:  sdburt@syr.edu

## Instructions

Reflection is a key activity of learning. It helps you build a strong metacognition, or "understanding of your own learning." A good learner not only "knows what they know", but they "know what they don't know", too. Learning to reflect takes practice, but if your goal is to become a self-directed learner where you can teach yourself things, reflection is imperative.

- Now that you've completed the assignment, share your throughts. What did you learn? What confuses you? Where did you struggle? Where might you need more practice?
- A good reflection is: **specific as possible**,  **uses the terminology of the problem domain** (what was learned in class / through readings), and **is actionable** (you can pursue next steps, or be aided in the pursuit). That last part is what will make you a self-directed learner.
- Flex your recall muscles. You might have to review class notes / assigned readings to write your reflection and get the terminology correct.
- Your reflection is for **you**. Yes I make you write them and I read them, but you are merely practicing to become a better self-directed learner. If you read your reflection 1 week later, does what you wrote advance your learning?

Examples:

- **Poor Reflection:**  "I don't understand loops."   
**Better Reflection:** "I don't undersand how the while loop exits."   
**Best Reflection:** "I struggle writing the proper exit conditions on a while loop." It's actionable: You can practice this, google it, ask Chat GPT to explain it, etc. 
-  **Poor Reflection** "I learned loops."   
**Better Reflection** "I learned how to write while loops and their difference from for loops."   
**Best Reflection** "I learned when to use while vs for loops. While loops are for sentiel-controlled values (waiting for a condition to occur), vs for loops are for iterating over collections of fixed values."

`--- Reflection Below This Line ---`

This assignment focused on building a multi-step ETL (Extract, Transform, Load) pipeline to process data from the Google Places API and Azure Cognitive Services. The pipeline extracts review data for given places, analyzes the sentiment of those reviews, and extracts named entities from the review text. This process demonstrates a common workflow in data engineering, where raw data is transformed into a structured format suitable for analysis.

The assignment involved several key components and steps. First, the apicalls.py module contains functions to interact with external APIs, including get_google_place_details() to fetch place details and reviews from the Google Places API, get_azure_sentiment() to analyze the sentiment of text using Azure Cognitive Services, get_azure_named_entity_recognition() to extract named entities from text, geocode() to geocode a place name, and get_weather() to fetch weather data for a location.

Second, the assignment_etl.py module implements the multi-step ETL process. The reviews_step() function takes place IDs as input (from a file or DataFrame), fetches place details and reviews using get_google_place_details(), transforms the data into a DataFrame with columns: place_id, name, author_name, rating, and text, and saves the DataFrame to CACHE_REVIEWS_FILE before returning it. The sentiment_step() function takes review data as input (from a file or DataFrame), analyzes the sentiment of each review using get_azure_sentiment(), transforms the data into a DataFrame with columns: place_id, name, author_name, rating, sentence_text, sentence_sentiment, and sentiment confidence scores, and saves the DataFrame to CACHE_SENTIMENT_FILE before returning it.  The  entity_extraction_step() function takes sentiment-annotated review data as input (from a file or DataFrame), extracts named entities from the review text using get_azure_named_entity_recognition(), transforms the data into a DataFrame with columns including the sentiment information, entity text, entity category, entity subcategory, and entity confidence scores, and saves the DataFrame to CACHE_ENTITIES_FILE before returning it.

Third, the assignment included testing with test_apicalls.py to test the individual API call functions in apicalls.py, and test_assignment_etl.py to test the output of the ETL pipeline steps, ensuring that the generated files have the correct data and structure.

Several challenges were encountered and addressed during this assignment.  A key challenge was ensuring the correct API key was used for the CENT iSchool IoT Portal and that it had the necessary permissions. Transforming the nested JSON responses from the APIs into flat DataFrames required careful use of pandas.json_normalize() and handling potential missing data or variations in the API responses.  Ensuring that modules were imported correctly, especially when running tests, required managing Python's module search paths (sys.path) and understanding how Python packages work (the __init__.py file).  This was a significant hurdle, and I learned the importance of explicit path management in Python projects.  Implementing robust error handling was crucial to prevent the pipeline from crashing due to API errors or unexpected data.  The code includes try...except blocks to catch potential exceptions and provide informative messages.  The ETL steps involved writing DataFrames to CSV files.  The code handles cases where no data is available, creating empty CSV files with the correct headers to satisfy the tests.

Through this assignment, I learned several important lessons. I gained a better understanding of the ETL process and how to break down a complex data processing task into smaller, manageable steps. I learned how to interact with RESTful APIs using the requests library, handle JSON data, and deal with API authentication. I improved my skills in using the pandas library for data manipulation, including reading and writing CSV files, transforming JSON data into DataFrames, and handling missing values. I learned the importance of anticipating and handling potential errors in data processing pipelines, especially when dealing with external systems like APIs. I gained a deeper understanding of how Python packages and modules work, and the importance of managing the sys.path to ensure correct imports, especially in the context of testing. Finally, I recognized the importance of writing comprehensive tests to verify the correctness of data processing code.