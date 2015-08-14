#!/usr/bin/env python
# Code: Connor Hornibrook, 04 August 2015
#
# Outputs a table of septic density values for every HUC11 watershed in
# the State of New Jersey. Created due to the limitations of the original
# NJDEP-created model, which allowed users to calculate density values by
# watershed on a municipality-wide basis, one at a time. While this can be
# useful in some ways, it would take hours to do calculations at different
# values for the entire state. This script does just that, usually in a matter
# of seconds.
#
# An understanding of the command line or git bash is needed in order to
# run this model, as it takes system arguments. 

import sys, os
from xlwt import *

# Dictionary containing average recharge values for all HUC11 watersheds
# in New Jersey. Data was taken from the publicly available DEP model which
# can be downloaded at http://www.nj.gov/dep/wqmp/docs/huc11_no3_cc_planning_tool_v3.0.xls
AVG_RECHARGE = {'02020007000' : (13.0, 'Rutgers Creek tribs'),
                '02020007010' : (13.9, 'Wallkill River (above road to Martins)'),
                '02020007020' : (13.7, 'Papakating Creek'),
                '02020007030' : (13.4, 'Wallkill River (below road to Martins)'),
                '02020007040' : (13.8, 'Pochuck Creek'),
                '02030101170' : (9.1, 'Hudson River'),
                '02030103010' : (13.4, 'Passaic River Upr (above Pine Bk br)'),
                '02030103020' : (12.9, 'Whippany River'),
                '02030103030' : (13.8, 'Rockaway River'),
                '02030103040' : (10.6, 'Passaic River Upr (Pompton to Pine Bk)'),
                '02030103050' : (15.0, 'Pequannock River'),
                '02030103070' : (15.3, 'Wanaque River'),
                '02030103100' : (13.2, 'Ramapo River'),
                '02030103110' : (11.9, 'Pompton River'),
                '02030103120' : (9.1, 'Passaic River Lower (Saddle to Pompton)'),
                '02030103140' : (9.2, 'Saddle River'),
                '02030103150' : (6.9, 'Passaic River Lower (Nwk Bay to Saddle)'),
                '02030103170' : (10.1, 'Hackensack R (above Hirshfeld Brook)'),
                '02030103180' : (5.5, 'Hackensack R (below/incl Hirshfeld Bk)'),
                '02030104010' : (0.2, 'Newark Bay / Kill Van Kull / Upr NY Bay'),
                '02030104020' : (5.4, 'Elizabeth River'),
                '02030104030' : (4.3, 'Morses Creek / Piles Creek'),
                '02030104050' : (7.1, 'Rahway River / Woodbridge Creek'),
                '02030104060' : (8.4, 'Raritan / Sandy Hook Bay tributaries'),
                '02030104070' : (11.6, 'Navesink River / Lower Shrewsbury River'),
                '02030104080' : (7.6, 'Shrewsbury River (above Navesink River)'),
                '02030104090' : (11.2, 'Whale Pond Bk / Shark R / Wreck Pond Bk'),
                '02030104100' : (12.3, 'Manasquan River'),
                '02030104910' : (4.6, 'Raritan Bay / Sandy Hook Bay'),
                '02030104920' : (9.1, 'Atlantic Coast (Sandy Hook to WhalePond)'),
                '02030104930' : (9.9, 'Atlantic Coast (Whale Pond to Manasquan)'),
                '02030105010' : (17.0, 'Raritan River SB (above Spruce Run)'),
                '02030105020' : (14.2, 'Raritan River SB (3 Brdgs to Spruce Run)'),
                '02030105030' : (11.0, 'Neshanic River'),
                '02030105040' : (11.9, 'Raritan River SB (NB to Three Bridges)'),
                '02030105050' : (16.0, 'Lamington River'),
                '02030105060' : (16.4, 'Raritan River NB (above Lamington)'),
                '02030105070' : (11.1, 'Raritan River NB (SB to Lamington)'),
                '02030105080' : (9.4, 'Raritan River Lower (Millstone to NB/SB)'),
                '02030105090' : (10.7, 'Stony Brook'),
                '02030105100' : (10.5, 'Millstone River (above Carnegie Lake)'),
                '02030105110' : (10.2, 'Millstone River (below/incl Carnegie Lk)'),
                '02030105120' : (9.7, 'Raritan R Lower (Lawrence to Millstone)'),
                '02030105130' : (9.1, 'Lawrence Brook'),
                '02030105140' : (12.0, 'Manalapan Brook'),
                '02030105150' : (10.7, 'Matchaponix Brook'),
                '02030105160' : (8.3, 'Raritan R Lower (below Lawrence)'),
                '02040104090' : (13.3, 'Shimers Brook / Clove Brook'),
                '02040104110' : (14.6, 'Walpack Bend / Montague Riverfront'),
                '02040104130' : (13.8, 'Little Flat Brook'),
                '02040104140' : (12.9, 'Big Flat Brook'),
                '02040104150' : (13.1, 'Flat Brook'),
                '02040104240' : (14.4, 'Van Campens Brook / Dunnfield Creek'),
                '02040105030' : (13.7, 'Trout Brook / Swartswood Lake'),
                '02040105040' : (13.8, 'Paulins Kill (above Stillwater Village)'),
                '02040105050' : (14.0, 'Paulins Kill (below Stillwater Village)'),
                '02040105060' : (13.6, 'Stony Brook / Delawanna Creek'),
                '02040105070' : (14.8, 'Pequest River (above/incl Bear Swamp)'),
                '02040105080' : (14.3, 'Bear Creek'),
                '02040105090' : (15.4, 'Pequest River (below Bear Swamp)'),
                '02040105100' : (13.9, 'Beaver Brook'),
                '02040105110' : (12.8, 'Pophandusing Brook / Buckhorn Creek'),
                '02040105120' : (11.5, 'Lopatcong Creek'),
                '02040105140' : (13.3, 'Pohatcong Creek'),
                '02040105150' : (14.1, 'Musconetcong River (above Trout Brook)'),
                '02040105160' : (15.0, 'Musconetcong River (below incl Trout Bk)'),
                '02040105170' : (12.5, 'Hakihokake/Harihokake/Nishisakawick Ck'),
                '02040105200' : (11.1, 'Lockatong Creek / Wickecheoke Creek'),
                '02040105210' : (11.0, 'Alexauken Ck / Moore Ck / Jacobs Ck'),
                '02040105230' : (11.1, 'Assunpink Creek (above Shipetaukin Ck)'),
                '02040105240' : (8.1, 'Assunpink Creek (below Shipetaukin Ck)'),
                '02040201030' : (0.4, 'Duck Creek and UDRV to Assunpink Ck'),
                '02040201040' : (9.3, 'Crosswicks Ck (above New Egypt)'),
                '02040201050' : (12.5, 'Crosswicks Ck (Doctors Ck to New Egypt)'),
                '02040201060' : (11.7, 'Doctors Creek'),
                '02040201070' : (8.2, 'Crosswicks Ck (below Doctors Creek)'),
                '02040201080' : (11.3, 'Blacks Creek'),
                '02040201090' : (9.8, 'Crafts Creek'),
                '02040201100' : (10.7, 'Assiscunk Creek'),
                '02040201110' : (8.0, 'Burlington/Edgewater Park Delaware tribs'),
                '02040202020' : (12.7, 'Rancocas Creek NB (above New Lisbon dam)'),
                '02040202030' : (15.0, 'Greenwood Branch (NB Rancocas Creek)'),
                '02040202040' : (10.8, 'Rancocas Creek NB (below New Lisbon dam)'),
                '02040202050' : (13.5, 'Rancocas Creek SB (above Bobbys Run)'),
                '02040202060' : (12.0, 'Rancocas Creek SB SW Branch'),
                '02040202070' : (10.5, 'SB Rancocas Creek (below Bobbys Run)'),
                '02040202080' : (8.2, 'Rancocas Creek'),
                '02040202090' : (8.3, 'Pompeston Creek / Swede Run'),
                '02040202100' : (6.8, 'Pennsauken Creek'),
                '02040202110' : (7.5, 'Cooper River'),
                '02040202120' : (8.0, 'Woodbury / Big Timber / Newton Creeks'),
                '02040202130' : (8.7, 'Mantua Creek'),
                '02040202140' : (7.7, 'Cedar Swamp / Repaupo Ck / Clonmell Ck'),
                '02040202150' : (9.1, 'Raccoon Creek / Birch Creek'),
                '02040202160' : (9.4, 'Oldmans Creek'),
                '02040206020' : (5.7, 'Pennsville / Penns Grove tribs'),
                '02040206030' : (9.2, 'Salem R(above 39d40m14s dam)/Salem Canal'),
                '02040206040' : (8.7, 'Salem River (below 39d40m14s dam)'),
                '02040206060' : (9.1, 'Alloway Creek / Hope Creek'),
                '02040206070' : (9.9, 'Stow Creek'),
                '02040206080' : (9.5, 'Cohansey River (above Sunset Lake)'),
                '02040206090' : (9.6, 'Cohansey River (below Cornwell Run)'),
                '02040206100' : (10.3, 'Back / Cedar / Nantuxent Creeks'),
                '02040206110' : (10.5, 'Dividing Creek'),
                '02040206120' : (10.1, 'Still Run / Little Ease Run'),
                '02040206130' : (10.4, 'Scotland Run'),
                '02040206140' : (9.7, 'Maurice River (above Sherman Ave Bridge)'),
                '02040206150' : (9.6, 'Muddy Run'),
                '02040206160' : (10.4, 'Maurice River (Union Lk to Sherman Ave)'),
                '02040206170' : (10.1, 'Maurice River (Menantico Ck to Union Lk)'),
                '02040206180' : (10.3, 'Menantico Creek'),
                '02040206190' : (11.2, 'Manamuskin River'),
                '02040206200' : (11.3, 'Maurice River (below Menantico Creek)'),
                '02040206210' : (11.1, 'West Creek / East Creek / Riggins Ditch'),
                '02040206220' : (10.7, 'Dennis Creek'),
                '02040206230' : (8.4, 'Cape May Tribs West'),
                '02040301020' : (13.1, 'Metedeconk River NB'),
                '02040301030' : (13.5, 'Metedeconk River SB'),
                '02040301040' : (10.3, 'Metedeconk River'),
                '02040301050' : (10.2, 'Kettle Creek / Barnegat Bay North'),
                '02040301060' : (14.6, 'Toms River (above Oak Ridge Parkway)'),
                '02040301070' : (14.5, 'Union/Ridgeway Branch (Toms River)'),
                '02040301080' : (13.6, 'Toms River (below Oak Ridge Parkway)'),
                '02040301090' : (14.6, 'Cedar Creek'),
                '02040301100' : (10.1, 'Barnegat Bay Central & Tribs'),
                '02040301110' : (14.6, 'Forked River / Oyster Creek'),
                '02040301120' : (11.4, 'Waretown Ck / Barnegat Bay South'),
                '02040301130' : (13.2, 'Manahawkin/Upper Little Egg Harbor tribs'),
                '02040301140' : (11.9, 'Lower Little Egg Harbor Bay tribs'),
                '02040301150' : (13.6, 'Basto River'),
                '02040301160' : (12.4, 'Mullica River (above Basto River)'),
                '02040301170' : (12.4, 'Mullica River (Turtle Ck to Basto River)'),
                '02040301180' : (14.9, 'Oswego River'),
                '02040301190' : (14.8, 'West Branch Wading River'),
                '02040301200' : (12.4, 'Mullica River (GSP bridge to Turtle Ck)'),
                '02040301210' : (8.7, 'Great Bay / Mullica R (below GSP bridge)'),
                '02040301910' : (3.7, 'Atlantic Coast (Manasquan to Barnegat)'),
                '02040301920' : (1.4, 'Atlantic Coast (Barnegat to Little Egg)'),
                '02040302010' : (5.8, 'Reeds Bay / Absecon Bay & tribs'),
                '02040302020' : (9.0, 'Absecon Creek'),
                '02040302030' : (10.8, 'Great Egg Harbor R (above HospitalityBr)'),
                '02040302040' : (11.4, 'Great Egg Harbor R (Lk Lenape to HospBr)'),
                '02040302050' : (11.2, 'Great Egg Harbor R (below Lake Lenape)'),
                '02040302060' : (7.6, 'Patcong Creek/Great Egg Harbor Bay'),
                '02040302070' : (11.0, 'Tuckahoe River'),
                '02040302080' : (7.6, 'Cape May Bays & Tribs East'),
                '02040302910' : (3.4, 'Atlantic Coast (Little Egg to Absecon)'),
                '02040302920' : (2.7, 'Atlantic Coast (Absecon to Great Egg)'),
                '02040302930' : (6.1, 'Atlantic Coast (Great Egg to 34th St)'),
                '02040302940' : (7.7, 'Atlantic Coast (34th St to Cape May Pt)')}

CALC_CONSTANT = 4.42
AR_INDEX = 0
WS_INDEX = 1


                                        # Standard values were used for all
                                        # of our project's calculations. 3.14
                                        # was our standard population density
                                        # but the DEP's model default was 3.0
        #save directory                 #std.: 2.0    #std.: 10.0
def main(outputDirectory, inPopDens, inTargetNO3, inLoadingRate):

    popDensity = float(inPopDens)
    targetNO3 = float(inTargetNO3)
    loadingRate = float(inLoadingRate)

    # creating the output file path with pop. density
    outputFile = outputDirectory + '\\NJ_NO3_values_%s.xls'%(str(popDensity))
    xl_rows = {}

    # populating the dictionary
    for huc11, values in AVG_RECHARGE.iteritems():
        avgRecharge = values[AR_INDEX]
        ws = values[WS_INDEX]
        sepdens = (CALC_CONSTANT * popDensity * loadingRate) / (avgRecharge * targetNO3)
        xl_rows[huc11] = (ws, avgRecharge, sepdens)

    wb = Workbook()
    writerSheet = wb.add_sheet('NO3_vals_%s_popdens'%(str(popDensity)))

    # writing headers
    writerSheet.write(0, 0, 'HUC11')
    writerSheet.write(0, 1, 'NAME')
    writerSheet.write(0, 2, 'AVGRECHRG')
    writerSheet.write(0, 3, 'SEPDENS')

    # writing the values to the new table
    row_index = 1
    for key, value in xl_rows.iteritems():
        ws = value[0]
        avgRecharge = value[1]
        sepdens = value[2]
        writerSheet.write(row_index, 0, key)
        writerSheet.write(row_index, 1, ws)
        writerSheet.write(row_index, 2, avgRecharge)
        writerSheet.write(row_index, 3, sepdens)
        row_index += 1

    wb.save(outputFile)
    os.startfile(outputFile)
    return xl_rows

# main method
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    
    
