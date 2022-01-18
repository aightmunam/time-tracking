# time-tracking

A time tracking application that allows users to keep track of their worked hours. 

### Basic functionality

Using the different apis provided, a user can 
- Create their account
- Create different contracts with different projects
- Add logs for different days depending on the hours worked under different contracts
- View and filter their logs

Admins are given special permissions, they can
- Create new projects
- View information of any users
- View contracts and logs of any user


### Database Design
The Database Design is as follows:

![Database design](https://github.com/aightmunam/time-tracking/blob/master/database-design.png?raw=true)

### Some future additions:

- Add an entity to represent Employers
- Reports for a time period (daily, weekly, quarterly etc)
  - How many total hours of work has been done by a user
  - How many total effort has been spent on a project by all users
  - Calculate how much an overall cost for an employer is
  - Calculate how much a user earns over a month working under multiple contracts
