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
12. status fields, is it activated, inactive or pending
