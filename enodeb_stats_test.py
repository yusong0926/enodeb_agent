import unittest
import enodeb_stats


class TestEnodebStatsMethods(unittest.TestCase):

    enodeblist_json = { 
       "EnodeBArray" :[
          {
           "eNBId"   : 591,                    
           "Description"   : "Maslak-12",      
           "Status"  : 1,                       
           "IpAddr"  : "10.1.49.200",         
           "GpsCoordinate" : {                
           "Latitude"  : 37.492425,          
           "Longitude" : 127.031008          
           },
           "ProfileArray" :[
             " Profile1",
             " Profile2",
             " Profile3"
           ]
          },
          {
           "eNBId"   : 592,                   
           "Description"   : "Maslak-12",      
           "Status"  : 1 ,                      
           "IpAddr"  : "10.1.49.200",          
           "GpsCoordinate" : {                 
           "Latitude"  : 37.492425,         
           "Longitude" : 127.031008        
           },
           "ProfileArray" :[
             " Profile1",
             " Profile2",
             " Profile3"
           ]
          }
       ]
    }
    enodebs = [591, 592]


    enodeb_stats_json = {
       "EnodeBStatsArray" :[
          {
             "Profile"  : "Profile-1",
             "StatsArray" :[
                 {
                    "Time"      :   123333,
                    "DlBitrate" :   10, 
                    "UlBitrate" :   20
                 },
                 {
                    "Time"      :   129333,
                    "DlBitrate" :   8,
                    "UlBitrate" :   0
                 }
              ]
          },
          {
              "Profile"  : "Profile-2",
              "StatsArray" :[
                 {
                    "Time"      :   121333,
                    "DlBitrate" :   12, 
                    "UlBitrate" :   21
                 },
                 {
                    "Time"      :   127333,
                    "DlBitrate" :   9,
                    "UlBitrate" :   1
                 }
                ]
          }
        ]
    }
    enodeb_stats_output=[{"enodeb":591, "profile":"profile-1", "time":123333, "dlbitrate":10, "ulbitrate" : 20}, 
                          {"enodeb":591, "profile":"profile-1", "time":129333, "dlbitrate":8, "ulbitrate" : 0},
                          {"enodeb":591, "profile":"profile-2", "time":121333, "dlbitrate":12, "ulbitrate" : 21},
                          {"enodeb":591, "profile":"profile-2", "time":127333, "dlbitrate":9, "ulbitrate" : 1}
                        ]
 


    def test_getEnodebs(self):
        result = enodeb_stats.get_enodebs(self.enodeblist_json)
        self.assertListEqual(self.enodebs, result)
    def test_getEnodebStats(self):
        result = enodeb_stats.get_enodeb_stats(self.enodeb_stats_json, 591)
        self.assertListEqual(self.enodeb_stats_output, result)

if __name__ == '__main__':
    unittest.main()
