---
title: "Playa Time Lapse Project"
date: 2011-09-15 12:00:00 +0000
---

*Originally published on [craneium.net](https://web.archive.org/web/20160315095018/http://craneium.net/)*

# Here is a link to the [video](https://web.archive.org/web/20160319063447/http://www.youtube.com/watch?v=ZQacfYW6eZQ "Video Link")!

# [Look at these amazing htHDR versions.](https://web.archive.org/web/20160319063447/http://bit.ly/BM_timelapse_fusions "htHDR Shots") ([tutorial link](https://web.archive.org/web/20160319063447/http://www.tolerableinsanity.com/blog/2011/10/hypertemporal-hdr-concept-hthdr/ "htHDR tutorial!"))

![htHDR image](/images/craneium/playa-timelapse/2011_09_02_21_25_45and1more_adjust2.jpg)

# On Saturday the 6th of August myself and three co-conspiritors hiked up to the top of old Razorback mountain. The hike is largely unremarkable save for the fact it overlooks the fine playa which serves as a home to burners everywhere. We had made this hike before to check on the Black Rock HAM radio repeater, a service offered by BRARA. This time we had a different project in mind. About 2 months previous, I had been given my first DSLR camera (see equipment list a bit further down), and had done several experiments with time-lapse photography around my new home at Langton Labs and during the 4th of Juplaya event.

The confluence of having seen this view of the playa from Old Razorback, and my newfound interest in photography got the engineer gears turning in my head. With the support of several friends, I decided to do a time-lapse video of the playa bringing the viewer from its pre-buring man state, through the event, and past the entire cleanup and GTFO efforts. This turned out to be a non-trivial, but extremely rewarding undertaking.

# Equipment Involved:

1 [Canon T1i DSLR camera](https://web.archive.org/web/20160319063447/http://www.dpreview.com/reviews/canoneos500d/ "Camera Link")

1 Walmart Special $50 car battery

1 [SunSaver Duo Charge Controller](https://web.archive.org/web/20160319063447/http://www.morningstarcorp.com/en/sun-saver-duo "Sun Saver Charge Controller")

2 LM317 based [voltage regulation circuits](https://web.archive.org/web/20160319063447/http://www.national.com/mpf/LM/LM317.html#Overview "Voltage Regulator Circuit") (soldered board free and coated in ["Liquid Tape"](https://web.archive.org/web/20160319063447/http://www.amazon.com/Plastic-Dip-LET14Z03-Liquid-Electrical/dp/B000LNKIFS "Liquid Tape Link"))

1 [Eye-Fi Pro X2 8 GB Class 6 SDHC Wireless Flash Memory Card EYE-FI-8PC](https://web.archive.org/web/20160319063447/http://www.eye.fi/products/prox2 "EyeFi Card")

1 [HQRP Kit AC Power Adapter and DC Coupler compatible with Canon Adapter](https://web.archive.org/web/20160319063447/http://www.amazon.com/HQRP-Adapter-Coupler-compatible-Digital/dp/B004APEF16/ref=cm_cr_pr_product_top "Camera Coupler")

1 [Powerfilm F15-1200 20w Folding Solar Panel Charger](https://web.archive.org/web/20160319063447/http://www.amazon.com/Powerfilm-F15-1200-Folding-Solar-Charger/dp/B002LCEQRI "Solar Panel ")

1 [Slik Heavy-Duty Tripod](https://web.archive.org/web/20160319063447/http://www.amazon.com/Slik-Heavy-Duty-Tripod-Fluid-Effect-Built-/dp/B00006HOKW/ref=sr_1_9?s=electronics&ie=UTF8&qid=1313790786&sr=1-9 "Tripod Link")

1 Cheap [Intervalometer](https://web.archive.org/web/20160319063447/http://www.amazon.com/Aputure-Powershot-Compatible-Inexpensive-Intervalometer/dp/B003Y35VJA)

# Planning and Setup:

The first thing we had to figure out was power. In my early tests with the camera, the current draw averaged around 200mA when taking photos every 10 minutes. This meant that we had to supply no less than 33 Amp Hours per week on the playa. Wishing to cover the entire 2 month span, this could be accomplished by small fleet of car batteries. However the idea of having to drag all that weight up 1600 feet above the playa sounded terrible, so I instead opted to get a single battery, supported by a backpacking solar panel and accompanying charge controller.

![Setup on the mountain](/images/craneium/playa-timelapse/2011-08-07_13-55-44_850.jpg)

Next up was bandwidth. Making a camera fire on a regular interval is pretty simple, but dealing with the gigabytes of generated data was less trivial. I did not want to compromise the size or quality of the images, but even a 32GB SD card would top out after a week of exposures at a reasonable rate. Thankfully, we have [friends in the area](https://web.archive.org/web/20160319063447/http://cq-blackrock.org/ "BRARA") who generously support a radio-linked point-to-point wifi back to Gerlach which is mirrored onto the internet. This combined with the "bottomless memory" feature that the new EyeFi SD cards support, enabled us to keep the data flowing!

After stringing all of the above equipment together in a logical fashion, we setup the repeater to turn on its wifi for several hours each day and tested everything. Then we went home!

# Annoying Reality:

EyeFi cards come with an extremely annoying, totally undocumented feature. Namely that they require a hardware reboot (or several) to delete photos. While we had planned to run this without any support, I (and several friends) ended up taking several trips up that way to reboot the thing! **Be warned EyeFi cards are not really optimal for this!** Some people have had luck with the CHDK and EyeFi, but sadly the T1i is not scriptable :(

# Photo Editing:

To go from 8000 x 12 magapixel images (22GB of data) to the movie you see here, I (Peretz) used:

1) Adobe Photoshop Lightroom - for batch photo editing

2) A time lapse settings export plugin -- slightly modified from one found here [http://www.pixiq.com/article/lightroom-timelapse-presets-now-updated-to-version-3](https://web.archive.org/web/20160319063447/http://www.pixiq.com/article/lightroom-timelapse-presets-now-updated-to-version-3) - to export two crop versions (zoomed in and widest setting) of the full video at ~30 fps.

3) iMovie - to add text, transition between the wide and the zoomed in views, tweak time (accelerating nights in the beginning and slowing time for the burns), and adding credits.

4) I also had access to a 6 core 3.5ghz, 24 gb RAM machine with a SSD drive, which made this go faster.

***

Now in more detail. (Btw, I am assuming you are familiar with the basic features and views of Lightroom.):

1) In Lightroom, I created a new catalog and imported all the image files. I set the cache size to 10 GB in Lightroom's preferences to make editing go much faster after a long import. When importing the files, I set "Render Previews" at 1:1. This automatically caches all size views of the photos and accelerates flipping through them later.

Since 8000 is too many photos to edit individually, I used Lightroom's batch editing features on groups of photos.

The first thing to do is to apply a crop to all of the photos. To select the crop constraints, consider your export medium. If it's youtube, you want to manually select a 16:9 (widescreen) aspect ratio for your crop box. Also, be sure not to crop lower than the resolution you intend to release at (whether it's 1080 or 720 etc.) Next select all of your photos in library/grid view. Go to develop view on one. Apply the crop. Now click the "Sync" button on the bottom right (if it's not there, go back to grid view and select all and return) and select only the "crop". This is the basic idea you will repeat on various groupings of photos with various settings being synchronized.

Within the Library view, I used the Metadata Filter to group photos by exposure settings. In our specific case, only the exposure time was automatically determined by the camera (with the other settings F-stop, ISO being fixed). So, for example, I could select all of the 30s exposures, and give them a keywords tag "night" and all of the exposures faster than 1/50 as "day" and all the rest as "medium".

For the first round, this grouping into three batches was sufficient. After selecting all of the photos within one batch, I chose one representative photo and took it to develop view. Primarily, for the day shots, I got rid of dust sports and aberrations that accumulated over the month of exposure to the elements. And for the night, I cleared up the dead pixels. And whatever else appealed to me aesthetically. Each time, I applied the edits to the whole group using the "sync" button.

As you can imagine, the transitions between day / mid / night were terrible, introducing jarring discontinuities. So I went through and selected those transitions and again gave them a keyword and edited them manually, smoothing the transition with a few frames on either side. I did have to scroll through 8000 photos, but in grid view at the maximally zoomed out setting, you can easily spot the discontinuities and manage this rather quickly. At the end, I probably edited 30 archetypical photos in all, but then shared those edit settings with various (and sometimes overlapping) groups.

2) To export the photo, I went to the "Slideshow" view of Lightroom. As suggested here [http://www.pixiq.com/article/lightroom-timelapse-presets-now-updated-to-version-3](https://web.archive.org/web/20160319063447/http://www.pixiq.com/article/lightroom-timelapse-presets-now-updated-to-version-3) I imported a custom User Template, BUT I DID NOT ALTER THE VIDEO PRESET. And I actually used search and replace in a text editor to modify their 29.97fps custom setting to 1920x1080 rather than the 1280 x 720 default. Then I exported using the standard 1080 export video setting of Lightroom. (This allows you to override LR seeming 10 frame a second limit, though I'm not sure wether this matters in the longrun, as the video program will make the final determination of frame rate (when you speed up and slow down.)

I did this twice for two different crops because I intended to switch between. (All of the photos and intermediate steps are available for download from the dropbox.) This took a long time, since until that point, Lightroom only recorded changed and edits in metadata. Only during this export, did it downsample the pictures

3) Imported both videos as events into iMovie. I'm assuming you don't need any how-tos from here, since the application is beginner friendly (and by that, I mean, to me.) I was going to fire up Adobe Premiere, but iMovie worked just fine.

4) Then I emailed my friend Sharps and asked him to compose a track!

Feel free to ask questions. Think of this as a living document!

# Kudos List:

Post-Processing : Peretz Partensky
Sound Composition : Sharps / Saedos Records ([http://sharpsbeats.com](https://web.archive.org/web/20160319063447/http://sharpsbeats.com/))
Hardware Providers: Todd Huffman and "Safety" Phil Lapsley

**Hike Team:**

Ted Blackman, Galit Sorokin, Giggity, Ryan "Flophouse" Matthews, Todd Huffman, Cody Daniel

**Special Thanks:**

BRARA Ham radio group ([http://blog.cq-blackrock.org/](https://web.archive.org/web/20160319063447/http://blog.cq-blackrock.org/))
Ranger Keeper (bandwidth down from the mountain)
Dropbox (for hosting raw images)
Langton Labs
