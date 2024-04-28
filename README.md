# CK Real Estate Application
This is a Django Application for CK Real Estate.  The main purpose of this project is to develop a custom real estate website. 
The high-level requirements for this custom website include a user-friendly interface for browsing through property listings, communication channels 
to allow clients reach out to real estate company, and links to help users explore the Omaha area and make educated buying decisions.  

## Pages Included
### Base HTML pages
1. base.html
2. base2.html
### Site Visitor Pages
1. home.html
2. all-listings.html
3. search-all-listing.html
4. profile.html
5. omahalinks.html
6. property-details.html
7. contact-realtor.html
8. share-property.html
9. contact_success.html
### Admin Site Pages
1. login.html
2. siteadminlanding.html
3. siteadminreports.html
4. update-profile.html
5. add-property.html
### CSS
1. base.css
2. base2.css
### Tables (Models)
1. Property_Type
2. Property_Neighborhood
3. Property_Status
4. Property_Price_Range
5. Property
6. Contact
7. Search_Log
## Page Information
### base.html 
This page is the base template for all the site visitor pages and incldues the CSS file base.css
- the top menu options include links to the Home, All Listings, Search All Listings, Profile, Omaha Links pages
- within the header of the website (right hand side) is a login button for the site admin that links to the login page
### base2.html 
This page is the base template for all the site admin pages and includes the CSS file base2.css
- includes header of the site admin pages and a logout button to logout the site admin 
### home.html 
This page is the landing page for the website for the site visitor.
- Included in views.py - def home
- it shows the featured and active property marked in the database
  - if no featured property is marked it will show a default cover photo
  - site visitor can see the featured property details by clicking a button that links to property-details.html
  - there should be a photo for the property displayed along with price, address, status, description, type and year built
    - all these fields are within the property table   
### all-listings.html
This page shows all the listings from the property table that is marked as active (property_active = True) for the site visitor.
- Included in views.py - def all_listings
- in table format with sorting and paging (5 listings per page), it shows from the property table:
  - property_title
  - property_price
  - neighborhood
  - home type
  - status
- site visitor should be able to click a button that links to property-details.html to view the specific property details
### search-all-listings.html
This page shows all the listings from the property table that is marked as active (property_active = True) for the site visitor,
as well as the search function by price range, neighborhood, and home type.
- Included in views.py - def seacrh_all_listings
- in table format with sorting and paging (5 listings per page), it shows from the property table:
  - property_title
  - property_price
  - neighborhood
  - home type
  - status
- site visitor should be able to click a button that links to property-details.html to view the specific property details
### profile.html
This page shows the profile for the Realtor.
- Included in views.py - def profile
### omahalinks.html
This page shows the site visitor things to do and places to eat at in Omaha, Ne.
### property-details.html
This page shows the site visitor the specific property details of a listing.
### contact-realtor.html
This page shows the site visitor a form to fill out to contact the realtor via email.
### share-property.html
This page shows the site visitor a form to fill out to contact the realtor via email about a specific property.
### contact_success.html
This pages shows the site visitor a thank you message after successfully submiting the contact-realtor.html or share-property.html forms.
### login.html
This page is the login in page for the site admin.
### siteadminlanding.html
This is the main page for the site admin and can only be accessed when the site admin is logged in.
### siteadminreports.html
This is the report page for the site admin and can only be accessed when the site admin is logged in.
### update-profile.html
This is the update profile page for the site admin and can only be accessed when the site admin is logged in.
### add-property.html
This is the add property page for the site admin and can only be accessed when the site admin is logged in.
