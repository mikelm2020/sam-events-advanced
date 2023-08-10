<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mikelm2020/sam-eventbridge">
    <img src="https://github.com/mikelm2020/video-streaming/blob/961be498851fc7b1e9d940550e7eb54ea3b2130f/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Serverless project with Amazon EventBridge</h3>

  <p align="center">
    A simple microservice application using AWS SAM, that uses Amazon EventBridge as at messaging between microservices.
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project has a simple application where you can send food orders to different restaurants based on an API Request. And using EventBridge each restaurant will recieve the right order. You can extend this just by adding more restaurants microservice. Each restaurant is in control of their EventBridge rule, in this way we keep the whole application very decoupled.
Also is used a microservice for send food orders to API Destination and control when events can't delivery, through a DLQ Dead Letter Queue for process the message later saving to DynamoDB Table.

## Architecture

![Basic Arquitecture](./diagrams/basic-arquitecture.png)

![API Destination Arquitecture](./diagrams/api-destinations-arq.png)

![DLQ Arquitecture](./diagrams/dlq-arquitecture.png)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Deploy the project

You will need to deploy each microservice individually - orderManager, pizzaHat and Thailand.

Also the microservice blueDragon for show API Destinations with the site https://webhook.site/

We will be using AWS SAM and make sure you are running the latest version - at the time of writing, this was 1.78.0 (sam --version).

Deploy the project to the cloud:

```
sam deploy --guided
```

When asked about functions that may not have authorization defined, answer (y)es. The access to those functions will be open to anyone, so keep the app deployed only for the time you need this demo running.

Next times, when you update the code, you can build and deploy with:

```
sam deploy
```

To delete the app:

```
sam delete
````

### Built With



* [![Python][Python]][Python-url]
* [![AWS][AWS]][AWS-url]
* [![Visual Studio Code][Visual Studio Code]][Visual Studio Code-url]

## AWS Services
* Amazon EventBridge
* Amazon API Gateway
* AWS Lambda
* AWS SAM
* AWS SDK Python
* Amazon SQS
* Amazon DynamoDB
* Amazon CloudWatch



<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->
## Contact

Miguel Angel López Monroy - 
[![linkedin][linkedin]][linkedin-url]
[![Gmail-shield][Gmail-shield]][Gmail-url]
[![Twitter-shield][Twitter-shield]][Twitter-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

My favorite resources used:

* [Python Documentation](https://docs.python.org/3.9/)
* [Blog Marcia Villalba](https://blog.marcia.dev/event-driven-applications)
* [AWS Documentation](https://docs.aws.amazon.com/es_es/index.html)



<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mikelm2020/sam-eventbridge.svg?style=for-the-badge
[contributors-url]: https://github.com/mikelm2020/sam-eventbridge/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mikelm2020/sam-eventbridge.svg?style=for-the-badge
[forks-url]: https://github.com/mikelm2020/sam-eventbridge/network/members
[stars-shield]: https://img.shields.io/github/stars/mikelm2020/sam-eventbridge.svg?style=for-the-badge
[stars-url]: https://github.com/mikelm2020/sam-eventbridge/stargazers
[issues-shield]: https://img.shields.io/github/issues/mikelm2020/sam-eventbridge.svg?style=for-the-badge
[issues-url]: https://github.com/mikelm2020/sam-eventbridge/issues
[license-shield]: https://img.shields.io/github/license/mikelm2020/sam-eventbridge.svg?style=for-the-badge
[license-url]: https://github.com/mikelm2020/sam-eventbridge/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555

[linkedin]: https://img.shields.io/badge/-LinkedIn-black.svg?style=flat-square&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/miguellopezmdev
[Gmail-shield]: https://img.shields.io/badge/Gmail-D14836?style=flat-square&logo=gmail&logoColor=white
[Gmail-url]: mailto:miguel.lopezm.dev@gmail.com
[Twitter-shield]: https://img.shields.io/badge/Twitter-%231DA1F2.svg?style=flat-square&logo=Twitter&logoColor=white
[Twitter-url]: https://twitter.com/miguellopezmdev

<!--[product-screenshot]: https://github.com/mikelm2020/video-streaming/blob/82a8c694a418723faacf992c5dd76b6e328120f8/api_playlists.png -->
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[AWS]: https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white
[AWS-url]: https://docs.aws.amazon.com/es_es/index.html
[Blog-url]: https://blog.marcia.dev/event-driven-applications
[Visual Studio Code]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
[Visual Studio Code-url]: https://code.visualstudio.com/
