#ifndef INPUTREADER_H
#define INPUTREADER_H

#include <opencv2/core/types.hpp>
#include <map>
#include <string>
#include <vector>


using namespace std;

class Map;

class InputReader {
    typedef pair<int, int> Match;

public:
	InputReader(const string &strSettingPath, const string &strMatchesPaths, const string &strImagesPath);
	int GetNumFrames();
	vector<int> GetImageBounds(cv::Mat K);
	cv::Mat GetK();
	vector<tuple<int,int,int> > GetInitialPairsFromMostMatches();
    vector<tuple<int,int,int> > GetInitialPairsFromQuartiles();
	vector<int> GetNotInitialFrames(int n);
	map<int, Match> GetMatches(int frameId1, int frameId2);
	map<int, cv::Point2f> GetPoints(int frameId);
	vector<cv::KeyPoint> GetKPs(int frameId);
	vector<cv::KeyPoint> GetUndistortedKPs(int frameId, cv::Mat K);
	vector<int> GetTrackIds(int frameId);
	string GetImageName(int frameId);
    const vector<int>& getAllTracks() const {return allTracks;}
	const map<int, vector<cv::Point2f> >& getKps() const {return kps;}
	void setKps(const map<int, vector<cv::Point2f> >& kps) {this->kps = kps;}
	const map<int, vector<int> >& getTrackIds() const {return track_ids;}
	void setTrackIds(const map<int, vector<int> >& trackIds) {track_ids = trackIds;}
	int getTrackCal1() const {return track_cal_1;}
	void setTrackCal1(int trackCal1) {track_cal_1 = trackCal1;}
	int getTrackCal2() const {return track_cal_2;}
	void setTrackCal2(int trackCal2) {track_cal_2 = trackCal2;}
	int getTrackVal1() const {return track_val_1;}
	void setTrackVal1(int trackVal1) {track_val_1 = trackVal1;}
	int getTrackVal2() const {return track_val_2;}
	void setTrackVal2(int trackVal2) {track_val_2 = trackVal2;}
	const map<int, string>& getImgNames() const {return img_names;}
	vector<int> GetIndexInKfs(vector<int>kfs, int track);
    void setFrame0(int f) {frame0 = f;}
    void setFrame1(int f) {frame1 = f;}
	int getFrame0() const {return frame0;}
	int getFrame1() const {return frame1;}
	const map<int, map<int, float> >& getRadios() const {return radios;}
	const map<int, string>& getLabels() const {return labels;}

	bool error;

protected:
	const string strSettingPath;
	const string strMatchesPath;
    const string strImagesPath;
	int numFrames;
    vector<int> allTracks;
    map<int, vector<cv::Point2f> > kps;
	map<int, vector<int> > track_ids;
	map<int, string> img_names;
	map<int, string> labels;
	map<int, map<int, float> > radios;

	int track_cal_1;
	int track_cal_2;
	int track_val_1;
	int track_val_2;
	int frame0;
	int frame1;

};
#endif // INPUTREADER_H;

