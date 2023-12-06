<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- [![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url] -->

[![LinkedIn][linkedin-shield]][linkedin-url]

<div align="center">
<h1 align="center">Space Academy</h1>
  <p align="center">
    GA SEI Project 4
    <br />
    <br />
    <a href="https://spaceacademy-frontend-production.up.railway.app/">View Live Site</a>

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
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#brief">Brief</a></li>
    <li><a href="#planning">Planning</a></li>
    <li><a href="#build-process">Build Process</a></li>
    <li><a href="#challenges-and-bugs">Challenges and Bugs</a></li>
    <li><a href="#key-takeaways">Key Takeaways</a></li>
    <li><a href="#future-improvements">Future Improvements</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
 
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

[![Product Name Screen Shot][product-screenshot]](https://spaceacademy-frontend-production.up.railway.app/)

Timeframe: 1 week
Team: Solo

This was fourth and final project of my General Assembly SEI course. The requirements were to use a **Django/python** backend with a **PostgreSQL** database, along with a **React** frontend. Being interested in ed-tech, I wanted my project to fall within this area. The final project is a gamified learning platform for children ages 8-16. Players explore planets, answer questions on various topics and use the rewards for those questions to upgrade their ship.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

- React.js
- Django
- Python
- Three.js
- React-Three-Fiber
- Postgresql
- Bootstrap
<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->

## Getting Started

### Prerequisites

- npm
  ```sh
  npm install npm@latest -g
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/jake-o-phillips/spaceacademy-backend.git
   ```
2. Install NPM packages
   ```sh
   npm install
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BRIEF -->

## Brief

- You will architect, design, and build a full-stack web app.
- It must be a full-stack **Django/React** application.
- Connect to and perform data operations on a **PostgreSQL** database (the default SQLLite3 database is not acceptable).
- Have at least 2 data Models, or 1 if consuming an external API
- Have **full-CRUD data operations** across any combination of the app's models (excluding the User model). For example, creating/reading/updating posts and creating/deleting comments qualifies as full-CRUD data operations.
- **Authenticate users using Django's built-in authentication**.
- **Implement authorization by restricting access to the Creation, Updating & Deletion of data resources** using the `login_required` decorator in the case of view functions; or, in the case of class-based views, inheriting from the `LoginRequiredMixin` class.
- Be **deployed online** using **Railway**. Presentations must use the deployed application.

In addition the basic requirements from GA, i also set myself some personal goals for this projects:
To be fully responsive and functional on mobile.
To incorporate my knowledge of Three.js and React Three Fiber

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- PLANNING -->

## Planning

I wanted to create something slightly different from a traditional CRUD app, so i decided to make a gamified learning platform with the goal of incentivising children and young adults to learn. Users would answer questions on a variety of topics, receiving rewards for correct answers which could be used to gain other perks. I was taking a course in three.js alongside the GA course so I also wanted to incorporate this knowledge, and I knew I could make a simple model of a solar system with clickable planets etc, so I decided on a Sci-Fi theme. I made an ERD which is included below, and decided to split the project into two Django apps, one for the learning part and the other for the game.

[![ERD Screen Shot][erd-screenshot]]

One of the decisions I had to make was who would provide the questions. On the one hand, I could make it so all users could post questions for other users. This allows for a huge and ever growing variety of questions, but makes it very difficult to moderate and make the game fair. On the other hand, I as the developer could write all the questions and be sure they give fair rewards, but this is a lot of extra work and limits the growth of the app. In the end I decided to take the latter option, with plans for the future to incorporate another type of user (moderators), who would be trusted individuals who would both update the questions and ensure the rewards were fair.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- BUILD PROCESS -->

## Build Process

### Decisions

To begin the project I made a number of decisions. I decided to use Django’s token based authentication as this seemed the simplest solution when working with a technology I was not very familiar with. I wanted my app to be fully responsive so I used bootstrap to leverage its container system. I also decided to get the backend working initially with minimal css, and implement styling afterwards.

### Authentication

The first task was implementing Django’s token based auth system. This went smoothly, but I soon realised that I needed to expand the default user model, so I made some additions that automatically assigned a custom user profile model to each user on registration. I also wrote a view to serve up this profile to the frontend when logging in.

```js
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        data = self.request.data

        username = data['username']
        password = data['password']
        re_password = data['re_password']

        if password == re_password:
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username already exists'})
            else:
                if len(password) < 6:
                    return JsonResponse({'error': 'Password must be atleas 6 characters'})
                else:
                    user = User.objects.create_user(username=username, password=password)
                    user.save()

                    user = User.objects.get(id=user.id)
                    print(user.username)
                    user_profile = UserProfile(user=user, username=user.username, first_name='', last_name='', experience=0, credits=0, prestige=0)
                    user_profile.save()
                    #assign ship
                    engines = Engines.objects.get(id=1)
                    shields = Shields.objects.get(id=1)
                    weapons = Weapons.objects.get(id=1)
                    thrusters = Thrusters.objects.get(id=1)

                    ship = Ship(user_profile=user_profile, name='Sirius', weapons=weapons, engines=engines, thrusters=thrusters, shields=shields)
                    ship.save()
                    return JsonResponse({'success': 'User created succesfully'})
        else:
            return JsonResponse({'error': 'Passwords do not match'})
```

The view to assign a custom user profile to each user

### Planets and Data Cards

The next task was to write routes and views for the 7 planned planets(subjects), returning their connected categories, question cards and questions. I also used react-router to switch between these pages and fetch the data on page-load. In all honesty, I tried to make my Django views as concise as I could, but I feel like there are so many possibilities in Django that there is almost certainly a better way of writing these views (They were mostly class based APIViews, as opposed to the viewsets that have a lot more functionality built in). At this point, even though I wasn’t completely finished with the backend I wanted to build out my UI a bit more.

### Frontend

I first built simple login and sign up pages and connected them up to the backend so that users could now sign up and log in. I created the map, planet, category and question views so that users could now experience the full chain of that interaction. I then implemented react router to navigate between pages. I wanted to build the 3d solar system map early to make sure I had time to change plans if it proved too difficult. Having created the planets and found their textures, it was not difficult to incorporate a close up spinning view of the planet in the planet view. I also used react-parallax-tilt and some CSS padding and overlaying to create some nice looking question cards.

### Logic

I still hadn’t written the backend logic for submitting the user’s individual answers, checking those answers against the correct answers in the database, and then again checking all the answers and calculating the reward when the user submits all their answers to unlock the data card. This involved writing a number of new views with checking logic on both the frontend and backend.

```js
class checkCardAnswers(APIView):
    def get(self, request, pk, question_card_id, format=None):
        user = self.request.user
        user = User.objects.get(id=user.id)

        #get all questions from question card
        question_card = QuestionCard.objects.get(id=question_card_id)
        questions = question_card.question_set.all()

        #for each question check if the user answer matches the correct answer
        reward_divider = 1
        try:
            for question in questions:

                userAnswer = Answer.objects.filter(user=user).get(question=question.id)
                if userAnswer:
                    print(question.correct_answer)
                    print(userAnswer)
                    if str(question.correct_answer) == str(userAnswer):
                        print('correct')
                    else:
                        reward_divider += 1
        except:
            return JsonResponse({'message': 'Answer all the questions'})

        #add credits and exp to profile
        profile = UserProfile.objects.get(user=user)
        credits_to_add = question_card.reward_credits / reward_divider
        profile.update_credits(credits_to_add)
        profile.update_experience(question_card.reward_exp)
        profile.save()
        #update locked cards
        new_locked_card = LockedCards.objects.create(user=user, question_card=question_card)
        new_locked_card.save()

        return JsonResponse({'reward divider': reward_divider,
                              'reward_experience' : question_card.reward_exp,
                              'reward_credits' : credits_to_add
                              })
```

The view for checking a user's answers and updating their profile

### User Profile

Now that the user’s profile could be updated with the rewards from correct answers, I wanted to display these attributes in my Navbar and have access to them across the whole app. I used react context to achieve this, combined with use effects to automatically update the information. I also changed my Navbar to conditionally render only the login/signup buttons if the user has no Django token (ie. not logged in), and the full information if there was a token in local storage.

### The Hangar

I wanted there to be a social aspect to my app, so having completed the ‘learn’ part of the app, I moved on to the ‘game’ part. This was written in a separate Django app with several new models for the ship, ship equipment and hangars. The hangars are similar to guilds in traditional MMO’s, and they alone incorporate full CRUD operations. I wrote routes and views so that users can create, join and leave hangars and view the other members. I also built a very simple post system for communication within these hangars. The UI for this page quickly became complicated and I realised I had made a mistake in not designing with mobile in mind when it came to making the site responsive.

### The Ship

I wanted the user to be able to use the rewards they gained, so I added ship models and ship equipment models to my database. I then wrote the routes to view and upgrade this equipment, with some simple logic on the frontend to check if the user had enough credits to upgrade the equipment. I found a 3d model on the internet and used react-three-fiber to load it into the screen for a more appealing and interactive UI

### Responsive Design

I had planned from the start to make my app usable on all devices, however, I didn’t spend enough time planning this for my first attempts at the UI. For future projects, I will strive to ensure the design is easily adaptable to all screens, possibly by designing for mobile first. Having said this, most of the UI was simple enough to need moderate adjustments. The Navbar and the Hangar page were the most difficult in this respect and required multiple custom breakpoints. I can see that a better utilisation of bootstrap containers and responsive elements would have helped if implemented from the beginning, however for this project I was still getting to grips with bootstrap so the CSS is a mixture of bootstrap and custom. This is a bit inelegant and i aim to improve it in future projects

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CHALLENGES AND BUGS -->

## Challenges and Bugs

### Authentication

The biggest challenge for me was implementing authentication using a technology i was completely new to. Django comes with a myriad of options for authentication so just choosing an appropriate one became a challenge in itself, and involved watching several tutorials. After having chosen Django’s token based authentication and seeing how it works, working through the documentation and implementing it went relatively smoothly.

### Responsive Design

As mentioned above, my lack of thorough planning when it came to designing my app for mobile caused me some frustrations later on and resulted in some convoluted code. It has however inspired me to further explore bootstrap and tailwind css in order to better understand how to more quickly and neatly incorporate responsive design.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Key Takeaways -->

## Key Takeaways

### React-three-fiber

I am very proud of the way the UI looks for this project, particularly the 3D elements. Prior to this project I had never used react-three-fiber, having only coded in three.js and the speed and ease that that framework allowed was a joy to work with.

I am also proud of the amount of content I was able to include in the app, exceeding the projects requirements for 2 data models. Due to my enjoyment and the efficiency of working with Django-Rest-Framework, I was able to implement 16 data models, many of which incorporated full CRUD functionality., along with an app that, although small, feels like a complete, stand-alone project.

These were my key takeaways for this project:

- **I really enjoy working with python/Django**
- **I really enjoy working with react-three-fiber**
- **I aim to plan my responsive design more thoroughly**
- **I aim to become adept with a css framework rather than always using custom css**

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- FUTURE IMPORVEMENTS -->

## Future Improvements

- Add a moderator user-type and come up with a design to allow them to write questions and set rewards.
- I am sure that my Django views are not the most efficient or easiest to read. I would like to explore Django further to really understand what is possible with this framework
- Having said this, because the app provides a complete user experience loop (explore, answer questions, upgrade ship, repeat), I may decide to leave this project unaltered as an example of what i can achieve in 1 week.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LICENSE -->

## License

Distributed under the MIT License.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- CONTACT -->

## Contact

Jake Phillips - jphillips@gmail.com

Portfolio Link: [Portfolio](https://github.com/jake-o-phillips/spaceacademy-backend)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[contributors-shield]: https://img.shields.io/github/contributors/jake-o-phillips/spaceacademy-backend.svg?style=for-the-badge
[contributors-url]: https://github.com/j-o-phillips/spaceacademy-backend/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/j-o-phillips/spaceacademy-backend.svg?style=for-the-badge
[forks-url]: https://github.com/j-o-phillips/spaceacademy-backend/network/members
[stars-shield]: https://img.shields.io/github/stars/jake-o-phillips/spaceacademy-backend/.svg?style=for-the-badge
[stars-url]: https://github.com/j-o-phillips/spaceacademy-backend/stargazers
[issues-shield]: https://img.shields.io/github/issues/spaceacademy-backend/spaceacademy-backend.svg?style=for-the-badge
[issues-url]: https://github.com/j-o-phillips/spaceacademy-backend/issues
[license-shield]: https://img.shields.io/github/license/spaceacademy-backend/spaceacademy-backend.svg?style=for-the-badge
[license-url]: https://github.com/j-o-phillips/spaceacademy-backend/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jake-phillips-developer/
[product-screenshot]: assets/readme/Display.png
[erd-screenshot]: assets/readme/erd.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com
