# Listings Microservice

**This microservice handles the creation of listings, links listings to category and is used by the "search_service" to find and categorize listings according to their categories**

## Tech Stack

| Core Libraries    |       Database       |
| ----------------- | :------------------: |
| PyMongo, Pydantic | Redis (TBD), MongoDB |

### Models

Listing Model Attributes as followed:

1. Consists of Two Classes, Listing and ListingUpdate
2. The id field is the primary key of the collection.
3. title, name of listing
4. display_images, an list of image url of listing images to be displayed to user
5. views, how many times the listing has been viewed
6. reference, used by users to refer to a specific listing
7. location, city where it is sold
8. account_id, user_id of owner of listing and is used to get more info on who's selling
9. category, type of listing eg, job posting (useful for dynamic layout at checkout where the listing will be shown to be different depending on the type)
10. additional_details, more information on the listing
11. promoted, listing owners can choose to promote and rank higher in search
12. status fields:
 <ol>
  <li>a. draft - when creating or editing a listing</li>
  <li>b. pending - when the listing is pending for an admin approval</li>
  <li>c. rejected - when an admin is rejecting an listing because of a reason as follows:</li>
  <ol>
   <li>c.1 the listing violated our terms and conditions</li>
   <li>c.2 the listing received a lot of reports on the site by other users and indeed a moderator sees that the listing is violating our terms and conditions</li>
   <li>c.3 the listing is incomplete</li>
   <li>c.4 other compliance reasons</li>
  </ol>
 <li>d. activated - when the listing is approved by an admin and is active on the site</li>
 <li>e. archived - when is expired, manually archived by an admin or by the listing owner</li>
 <li>f. purged - will be still kept in our database for another 30 days after deletion from the site but it will not be displayed on the site both frontend and admin panel - after this period this listing will be permanently deleted</li>
</ol>
  
