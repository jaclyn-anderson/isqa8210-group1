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
### Models(Tables)
- class Property_Type
- class Property_Neighborhood
- class Property_Status
- class Property_Price_Range
- class Property
- class Contact
- class Search_Log
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
- this page shows the property featured (property_featured=True) and active (property_active=True) in the property table
  - the site visitor can see the featured property details by clicking a button that links to property-details.html
  - Fields displayed on the page from the property table
    - property_photo1
    - property_price
    - property_street address
    - property_city
    - property_state
    - property_zip_code
    - status
    - property_description
    - home_type
    - property_year_built
  -if no property is marked featured and active in the property table a default cover photo is shown  
### all-listings.html
This page shows all the listings from the property table that is marked as active (property_active = True) for the site visitor.
- Included in views.py - def all_listings
- in table format with sorting and paging (5 listings per page), it shows from the property table:
  - property_title
  - property_price
  - neighborhood
  - home type
  - status
- the site visitor should be able to click a button in the row of a property listing that links to property-details.html to view the specific property details
### search-all-listings.html
This page shows all the listings from the property table that is marked as active (property_active = True) for the site visitor, as well as the search function by price range, neighborhood, and home type.
- included in views.py - def seacrh_all_listings
- in table format with sorting and paging (5 listings per page), it shows from the property table:
  - property_title
  - property_price
  - neighborhood
  - home type
  - status
- the site visitor should be able to click a button in the row of a property listing that links to property-details.html to view the specific property details
### profile.html
This page shows the profile for the Realtor.
- included in views.py - def profile
- all fields from the contact table should be included on this page are listed below (note: only one contact should be in the contact table):
  - contact_first_name
  - contact_last_name
  - contact_phone
  - contact_email
  - contact_website_link
  - contact_office_street_address
  - contact_office_city
  - contact_office_state
  - contact_office_zip_code
  - contact_profile_image
  - contact_profile_description
- default contact information will be provided for initial rollout and should be updated by real estate agent when deployed
### omahalinks.html
This page shows the site visitor things to do and places to eat at in Omaha, Ne. not edittable by site admin
### property-details.html
This page shows the site visitor the specific property details of a listing.
- included in views.py - def property_details
- all fields for a specific property from the property table should be included on this page are listed below:
  - property_photo1
  - property_photo2 (not required)
  - property_photo3 (not required)
  - property_photo4 (not required)
  - property_price
  - property_street address
  - property_city
  - property_state
  - property_zip_code
  - status
  - property_description
  - home_type
  - property_year_built
  - neighborhood
  - property_area
  - property_bedroom_count
  - property_bathroom_count
- the site visitor should be able to click a button on this page that links to share-property.html to contact the realtor about this specific property
### contact-realtor.html
This page shows the site visitor a form to fill out to contact the realtor via email.
- incldued in views.py - def contact-realtor
- the site visitor show have the following fields to fill out on the form:
  - Name
  - Phone
  - Email
  - Comments/Questions
- the site visitor should be able to click send email button to send all fields on the form to the realtor and be redirected to the contact_success.html when successful  
### share-property.html
This page shows the site visitor a form to fill out to contact the realtor via email about a specific property.
- incldued in views.py - def contact-realtor
- included in forms.py - class ContactForm
- the site visitor show have the following fields to fill out on the form:
  - Name
  - Phone
  - Email
  - Property-detail link (readonly prefilled with correct property-detail link)
  - Comments/Questions
- the site visitor should be able to click send email button to send all fields on the form to the realtor and be redirected to the contact_success.html when successful
### contact_success.html
This pages shows the site visitor a thank you message after successfully submiting the contact-realtor.html or share-property.html forms.
- included in views.py - def contact_success
### login.html
This page is the login in page for the site admin.
### siteadminlanding.html
This is the main page for the site admin and can only be accessed when the site admin is logged in.
- included in views.py - def siteadminlanding
### siteadminreports.html
This is the report page for the site admin and can only be accessed when the site admin is logged in.
- included in views.py - def siteadminreports
### update-profile.html
This is the update profile page for the site admin and can only be accessed when the site admin is logged in.
- included in views.py - def update_profile
- included in forms.py - class ProfileForm
### add-property.html
This is the add property page for the site admin and can only be accessed when the site admin is logged in.
- included in views.py - def add_property
- included in forms.py - class PropertyForm
