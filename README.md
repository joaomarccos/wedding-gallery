# wedding-gallery

![Workflow Status](https://img.shields.io/github/workflow/status/joaomarccos/wedding-gallery/Deploy%20to%20Amazon%20ECS/master)

## Stack and Technologies:
 1. Python Language 
 2. Flask (Bootstrap + Security)
 3. MongoDB (MongoDB Atlas Cluster)
 4. AWS (S3, ECR, ECS)
 5. Github Actions
  
## Model
Example of document to represent a photo on gallery:  
```json
{
    "_id":"5df2de20134e8409c41644fa",
    "author" : "João",
    "url" : "https://wedding-gallery-bkt.s3.amazonaws.com/d92f5b6a774945e49fc723a15...",
    "active" : true,
    "timestamp" : "2019-12-12T21:41:01.413+00:00",
    "likes" : 21
}
```
 
## Auto Deploy to Amazon ECS
Using github actions to deploy the app on Amazon Elastic Cluster Service
    
on master commit: 
 - Build, tag, and push image to Amazon ECR
 - Fill in the new image ID in the Amazon ECS task definition
 - Deploy Amazon ECS task definition

<!---
### [Clik here to view running - http://3.215.179.89/](http://3.215.179.89/)

Use the users bellow to approve new photos:
    
    email: joao
    password: 123
    
    or
    
    email: maria
    password: 123 
   
-->
