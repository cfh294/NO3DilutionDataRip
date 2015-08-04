# NO3DilutionDataRip tool
## The DEP Model 
The NJDEP HUC11 Nitrate Planning Tool is a publicly available Microsoft Excel model that was created in order
to calculate various values associated with Nitrate Dilution standards in New Jersey. The DEP's model allows
the user to select a municipality and input various parameters regarding NO3 dilution. The model then lists all 
watersheds that fall within the selected municipality and the calculated septic density and average recharge values 
(these are calculated using the parameters input by the user). 

## Why I made this complimentary script
Pulling data by municipality can take forever! What if you wanted to use the model for every watershed in the state
at different input parameters. That would be 565 municipalities (well, not really, because the model covers all but
Hudson and Essex Counties) FOR EACH set of different parameters. First I tried to create an xlrd-heavy tool that 
iterated through the municipality-selector drop-down box. Long story short: I'm pretty sure xlrd can't do that yet. 
Instead, I played around with the model to see how it was making it's calculations. Using xlrd and xlwt, my script 
shoots out a new statewide sheet that has all watersheds. 

## How to use it
Run it from the command line using system arguments as the parameters (check out the source code for 
more specific info). 

## GIS?
The output list has a HUC11 join field that can easily be joined to a watershed shapefile or feature class. I was 
going to write this into my script, but I realized that this tool could be used outside of arcpy and GIS, as well. 


###Disclaimer: 
I did not create the original DEP model! It can be downloaded from this repo, or by going to: 

                         http://www.nj.gov/dep/wqmp/docs/huc11_no3_cc_planning_tool_v3.0.xls

