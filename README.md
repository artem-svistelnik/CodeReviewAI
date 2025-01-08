# CodeReviewAI

*To start the project you need to execute:**

* clone project repo in empty directory
* Create an .env file and populate it following the default.env file example

* execute the command `make build`
* execute the command `make run`


you can check swagger on http://0.0.0.0:8080/docs


you can run health check on GET http://0.0.0.0:8080/health

you can make a review on POST http://0.0.0.0:8080/review

you can see logs in you terminal


### Part 2 - What If

**Handling 100+ new review requests per minute:**

To scale the system to handle high traffic, I would utilize a message queue like RabbitMQ or Kafka to decouple the review requests and distribute the load across multiple worker instances. This ensures that requests are processed asynchronously and can be retried in case of failures. 

**Handling large repositories with 100+ files:**


When scanning large repositories with 100+ files, file handling efficiency is key to avoid memory overload. We can process the files streaming them rather than loading them entirely into memory. This ensures that the system can scale for large repositories without being constrained by memory limitations.

Since processing a large repository involves analyzing each file for code quality, dependencies, and other review metrics, we can distribute the work across multiple worker nodes. By using a task queue like Celery in combination with Redis for managing worker queues, we can delegate the review tasks for different files in parallel. This increases throughput and minimizes the total time required to review large repositories.

**Managing API Usage (OpenAI and GitHub)**

We could also consider batching requests to GitHub and OpenAI, so instead of querying each repository or file individually, we can group multiple requests together to minimize overhead and reduce costs.