# Generative AI
Generative AI or GenAI, is an AI that can create new content such as text, images,video and software code in response to a user's prompt.

### Types of GenAI(based on the output content):
1) Text - Large Language Models can generate text to write articles, summarize documents or draft emails.
2) Images - Diffusion models or GANs can create digital art and photrealistic photos.
3) Audio - This is created for voice-assistants, music composition, sound effects and voice cloning.
4) Code - Just like text, LLMs can also generate code.

### How GenAI works?
For the most part, generative AI operates un three phases:
**Training**, to create a foundation model that can serve as basis of multiple gen AI applications.
**Tuning**, to tailor the foundation model to a specific gen AI application.
**Generation** to access the gen AI application's output and continually improve its quality and accuracy.

#### Training
GenAI begins with a foundation model, a deep learning model that serves as a basis for multiple different types of gen AI applications. The most common foundation models today are large language models(LLMs). 
To create a foundation model, practitioners train a deep learning algorithm on huge vlumes of raw, unstructured, unlabeled data. During training, the algorrithm performs and evaluates millions of "trying to predict next element in a sequence" exercises, like next word in a sentence or next element in an image or next command in a line of code and continuously tries to minimize the difference between its predictions and actual/correct data.

The result of this training is a neural network of parameters, encoded representation of patterns and relationships in the data thhat can generate content autonomously in response to inputs or prompts.

#### Tuning
The foundation model is a generalist, so it knows about a lot of different types of content but often can't generate specific types of output with desired accuracy. So the model must be trained to a specific content generation task.

##### Fine tuning
Fine tuning involves feeding the model labeled data specific to content generation application questions or prompts the application is likely to receive, and corresponding correct answers in the desired format. For example: to create a customer service chatbot, developers would create hundreds or thousands of documents containing labeled customers service questions and correct answers and feed those to the model.

#### Generation
Developers and users continually assess the outputs of their generative AI apps and further tune the model for greater accuracy or relevance.