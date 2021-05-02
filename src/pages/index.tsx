import React from "react";
import styles from "./index.css";
import './index.css';
import axios from 'axios';
import { DateTimePickerComponent } from '@syncfusion/ej2-react-calendars';
import { gapi } from 'gapi-script';

import { Layout, Menu, Icon, Card, Radio, Select, Badge, Button } from "antd";
import { Pie } from "ant-design-pro/lib/Charts";
import "ant-design-pro/dist/ant-design-pro.css"; // Import whole style

const { Header, Content, Footer, Sider } = Layout;

import { formatMessage } from "umi-plugin-locale";
import { connect } from "dva";

//mapstyle, change to dark matter
import mapStyle from "../assets/style.json";
import { fromJS } from "immutable";

import MapGL from "react-map-gl";
import { GlobalState } from "@/common/types";

import {
  CurbFeature,
  CurbFeatureCollection,
  filterCurblrData //TODO FILTER DAY MONTH
} from "@/common/curblr";
import {
  FeatureCollection,
  featureCollection,
  feature,
  LineString
} from "@turf/helpers";

import { actions as curblrActions, geoDataFiles } from "../models/curblr";
import { TouchPitchHandler } from "mapbox-gl";

var mapboxAccessToken =
  "pk.eyJ1Ijoic2FhZGlxbSIsImEiOiJjamJpMXcxa3AyMG9zMzNyNmdxNDlneGRvIn0.wjlI8r1S_-xxtq2d-W5qPA";

//loads map style
const defaultMapStyle = fromJS(mapStyle);

//sunset
// const MAXSTAY_COLOR_MAP:{ [key: string]: any } = {
//     "3": "#FFDF00",
//     "15": "#F1B408",
//     "30": "#F1871C",
//     "60": "#F06121",
//     "120": "#F12627",
//     "180": "#C80286",
//     "240": "#63238A",
// }

//opposite of sunset
// const MAXSTAY_COLOR_MAP:{ [key: string]: any } = {
//     "3": "#FFDF00",
//     "15": "#8BBA25",
//     "30": "#018D5A",
//     "60": "#00A8C4",
//     "120": "#1078C3",
//     "180": "#4336A2",
//     "240": "#6D238A",
// }

//blues
const MAXSTAY_COLOR_MAP: { [key: string]: any } = {
  "3": "#e1f5fe",
  "15": "#81d4fa",
  "30": "#4fc3f7",
  "60": "#03a9f4",
  "120": "#0277bd",
  "180": "#01579b",
  "240": "#00345D"
};

//greens
// const MAXSTAY_COLOR_MAP:{ [key: string]: any } = {
//     "3": "#ffee58",
//     "15": "#cddc39",
//     "30": "#7cb342",
//     "60": "#689f38",
//     "120": "#388e3c",
//     "180": "#1b5e20",
//     "240": "#124116",
// }

const ACTIVITY_COLOR_MAP = {
  "no standing": "#777777",
  "no parking": "#DD2C00",
  "passenger loading": "#FF9100",
  "loading": "#FFEA00",
  "transit": "#37B34A",
  "free parking": "#00E5FF",
  "paid parking": "#2979FF",
  "restricted": "#AA00FF"
};

const scaledOffset = (offset: number) => {
  return {
    type: "exponential",
    base: 2,
    stops: [
      [12, offset * Math.pow(2, 12 - 16)],
      [16, offset * Math.pow(2, 16 - 16)]
    ]
  };
};

const scaledWidth = (width: number) => {
  return {
    type: "exponential",
    base: 2,
    stops: [
      [12, width * Math.pow(2, 12 - 16)],
      [16, width * Math.pow(2, 16 - 16)]
    ]
  };
};

const dataLayer = fromJS({
  id: "dataLayer",
  source: "curblrData",
  type: "line",
  interactive: true,
  paint: {
    "line-color": ["get", "color"],
    "line-offset": ["get", "offset"],
    "line-width": scaledWidth(6.8)
  }
});

// sets average parking length (roughly 7m, per NACTO) for use in estimating length in # of parking spaces
const avgParkingLength = 7;


const renderCurblrData = (
  data: CurbFeatureCollection,
  day: string,
  time: string,
  filterType: string
): FeatureCollection<LineString> => {
  var renderData = featureCollection<LineString>([]);
  var filteredData = filterCurblrData(data, day, time);//TODO FILTER DAY MONTH

  for (var curbFeature of filteredData.features) {
    var renderFeature = feature<LineString>(curbFeature.geometry);
    renderFeature.properties = {};

    for (var regulation of curbFeature.properties.regulations) {
      // marks each feature with its length
      renderFeature.properties.length =
        curbFeature.properties.location.shstLocationEnd -
        curbFeature.properties.location.shstLocationStart;

      renderFeature.properties.priority = regulation.priority;

      var priority = renderFeature.properties.priority;
      // if(priority) {
      var offsetPriority = 0;
      //offsetPriority = (10 * priority);

      var baseOffset = 10 + offsetPriority;
      if (curbFeature.properties.location.sideOfStreet === "left")
        baseOffset = 0 - 10 - offsetPriority;

      renderFeature.properties["offset"] = baseOffset; //scaledOffset(baseOffset);

      if (filterType === "maxStay") {
        if (regulation.rule.maxStay) {
          var maxStay = regulation.rule.maxStay + "";
          if (MAXSTAY_COLOR_MAP[maxStay]) {
            renderFeature.properties["color"] = MAXSTAY_COLOR_MAP[maxStay];
            renderFeature.properties.maxStay = maxStay;
            renderData.features.push(renderFeature);
          }
        }
      }
      // Splits out common activities and variants for an overall view. Features that fall into more than one "bucket" are duplicated, but handled by ensuring that they ultimately fall into the more specific bucket via painter's algorithm.
      // Requires ts.3.7 because of null arrays - I lucked out on mine but this will break on a different environment
      else if (filterType === "activity") {

        if (regulation.rule.activity === "no parking") {
          renderFeature.properties["color"] =
            ACTIVITY_COLOR_MAP["no parking"];
          // set the activty to use later in hooking up chart to map data
          renderFeature.properties.activity = "no parking";
          renderData.features.push(renderFeature);
        }
        if (
          regulation.rule.activity === "no standing"
        ) {
          renderFeature.properties["color"] =
            ACTIVITY_COLOR_MAP["no standing"];
          // set the activty to use later in hooking up chart to map data
          renderFeature.properties.activity = "no standing";
          renderData.features.push(renderFeature);
        }
        if (
          regulation.rule.activity === "parking" &&
          !regulation.rule.payment &&
          !regulation.userClasses?.some(uc => uc.classes?.length > 0)
        ) {
          renderFeature.properties["color"] =
            ACTIVITY_COLOR_MAP["free parking"];
          renderFeature.properties.activity = "free parking";
          renderData.features.push(renderFeature);
        }
        if (
          regulation.rule.activity === "parking" &&
          regulation.rule.payment &&
          !regulation.userClasses?.some(uc => uc.classes?.length > 0)
        ) {
          renderFeature.properties["color"] =
            ACTIVITY_COLOR_MAP["paid parking"];
          renderFeature.properties.activity = "paid parking";
          renderData.features.push(renderFeature);
        }
        if (regulation.rule.activity === "loading") {
          renderFeature.properties["color"] = ACTIVITY_COLOR_MAP["loading"];
          renderFeature.properties.activity = "loading";
          renderData.features.push(renderFeature);
        }
        if (
          regulation.userClasses?.some(uc =>
            [
              "motorcycle",
              "hotel guest",
              "permit",
              "reserved",
              "handicap",
              "scooter",
              "bicycle",
              "USPS",
              "car share",
              "police",
              "tour bus"
            ].some(c => uc.classes?.includes(c))
          )
        ) {
          renderFeature.properties["color"] =
            ACTIVITY_COLOR_MAP["restricted"];
          renderFeature.properties.activity = "restricted";
          renderData.features.push(renderFeature);
        }
        if (
          regulation.userClasses?.some(uc =>
            ["taxi", "passenger", "TNC", "rideshare"].some(c =>
              uc.classes?.includes(c)
            )
          )
        ) {
          renderFeature.properties["color"] =
            ACTIVITY_COLOR_MAP["passenger loading"];
          renderFeature.properties.activity = "passenger loading";
          renderData.features.push(renderFeature);
        }
        if (
          regulation.userClasses?.some(uc => uc.classes?.includes("transit"))
        ) {
          renderFeature.properties["color"] = ACTIVITY_COLOR_MAP["transit"];
          renderFeature.properties.activity = "transit";
          renderData.features.push(renderFeature);
        }
      }
    }
  }

  return renderData;
};

const mapStateToProps = (d: GlobalState) => {
  return d.curblr;
};

type PageStateProps = ReturnType<typeof mapStateToProps>;

type PageProps = PageStateProps;

class Map extends React.Component<PageProps, {}> {
  _mapRef: any;

  state = {
    mode: "activity",
    day: "mo",
    time: "08:01",
    mapStyle: defaultMapStyle,
    viewport: {
      width: "100vw",
      height: "100vh",
      // needs update? default viewport is hard-coded and should dynamically set based on data. PHL viewport:
      //        latitude:  39.950,
      //        longitude:-75.174, //-71.20566699900684,46.81214413176751 - QUEBEC
      //        zoom: 16
      // PDX viewport 
      // latitude: 46.81214413176751,
      // longitude: -71.20566699900684,
      latitude: 45.5322288090008, 
      longitude: -73.63143205202765,
      zoom: 13
    },
    showHideCard: true,
    sl_arrondRef: "plaza",
    set_dateTimeRef: new Date(),
    data_to_replace: new CurbFeatureCollection(),
    old_VS_new_selector: false
  };

  constructor(props: any) {
    super(props);
    this.hideComponent = this.hideComponent.bind(this);
    this.setArrond =  this.setArrond.bind(this);
    this.setDateTime = this.setDateTime.bind(this);
    this._mapRef = React.createRef();
  }

  _setMapData = (newData: any) => {
    const map = this._getMap();
    if (map) {
      map.getSource("curblrData").setData(newData);
    }
  };

  _getMap = () => {
    return this._mapRef ? this._mapRef.current.getMap() : null;
  };


  componentDidMount() {
    this._loadData();

    const map = this._getMap();

    if (map) {
      // TODO doesn't fire due to overlays div
      map.on("mouseover", "dataLayer", function(e) {
        console.log({ e });
        var coordinates = e.features[0].geometry.coordinates.slice();
        var description = e.features[0].properties.description;

        // Ensure that if the map is zoomed out such that multiple
        // copies of the feature are visible, the popup appears
        // over the copy being pointed to.
        while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
          coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
        }

        // TODO needs work
        // new mapboxgl.Popup()
        // .setLngLat(coordinates)
        // .setHTML(description)
        // .addTo(map);
      });
    }

    window.onresize = () => {
      const { viewport } = this.state;
      this.setState({
        viewport: {
          ...viewport,
          width: window.innerWidth,
          height: window.innerHeight
        }
      });
    };
  }

  componentWillUnmount() {
    window.onresize = null;
  }

  _loadData() {
    const mapStyle = defaultMapStyle
      // Add geojson source to map
      .setIn(
        ["sources", "curblrData"],
        fromJS({
          type: "geojson",
          data: renderCurblrData(
            this.props.curblr.data,
            this.state.day,
            this.state.time,
            this.state.mode
          )
        })
      )
      // Add point layer to map
      .set("layers", defaultMapStyle.get("layers").push(dataLayer));

    this.setState({ mapStyle });
  }

  changeTime = (value: any) => {
    this.setState({ time: value });

    var data = renderCurblrData(
      this.props.curblr.data,
      this.state.day,
      value,
      this.state.mode
    );
    this._setMapData(data);
  };

  changeDay = (value: any) => {
    this.setState({ day: value });

    var data = renderCurblrData(
      this.props.curblr.data,
      value,
      this.state.time,
      this.state.mode
    );
    this._setMapData(data);
  };

  changeMode = (event: any) => {
    this.setState({ mode: event.target.value });

    var data = renderCurblrData(
      this.props.curblr.data,
      this.state.day,
      this.state.time,
      event.target.value
    );
    this._setMapData(data);
  };
//TODO
  changeGeoData = async (value) => {

    this.state.old_VS_new_selector = false;
    await this.props.dispatch(curblrActions.fetchGeoData(value));
    console.log('day changeGeoData', this.state.day)
    console.log('time changeGeoData', this.state.time)
    console.log('mode changeGeoData', this.state.mode)

    var data = renderCurblrData(
      this.props.curblr.data,
      this.state.day,
      this.state.time,
      this.state.mode
    );
    this._setMapData(data);
  };

  changeGeoDataFromPost = async (data_awaited) => {
  
    this.state.old_VS_new_selector = true;
    const data_fetched_njson = await data_awaited;
    var data = renderCurblrData(
      data_fetched_njson,
      this.state.day,
      this.state.time,
      this.state.mode
    );
    this._setMapData(data);
  };
  //-----------------------------------
  
  hideComponent(name) {
    switch (name) {
      case "showHideCard":
        this.setState({ showHideCard: !this.state.showHideCard });
        break;
      default:
        null;
    }
  }

  setDateTime = (sl_arrondRef) => {
    this.setState({ sl_arrondRef });
    console.log(`Option selected:`, sl_arrondRef.value);
  }
  setArrond = (set_dateTimeRef) => {
    this.setState({ set_dateTimeRef });
    console.log(`Option selected:`, set_dateTimeRef.value);
  }
  sendRequest= () =>{
    this.state.old_VS_new_selector = true;

    let uri = "http://127.0.0.1:8081/items";

    const payload = {
      "true_date_time": this.state.set_dateTimeRef,
      "arrond_quartier": this.state.sl_arrondRef,
      "price": 3,
      "minStay": 32
    }
      axios.post(uri, payload)
      .then((response) => {
        console.log(response);
        // this.state.data_to_replace = response.data;
        console.log(response.data);
        
      // this.props.curblr.data = response.data;
      this.state.data_to_replace = response.data;
      this.changeGeoDataFromPost(response.data);
      }, (error) => {
        console.log(error);
      });
  };
  handleChange = (name, event) => {
    const target = event.target; // Do we need this?(unused in the function scope)!
    this.setState({
      [name]: event.target.value
    }, () => {
      console.log(this.state.sl_arrondRef);
      console.log(this.state.set_dateTimeRef)
      // Prints the new value.
    });
  };

  render() {
    const { viewport, mapStyle, day, time, mode, showHideCard, sl_arrondRef, set_dateTimeRef, data_to_replace, old_VS_new_selector} = this.state;

  // shows everything. would be great if this could intersect the feature collection with the viewport bounding box. i can't figure it out. for kevin?
  const dt_to_set = (old_VS_new_selector? data_to_replace : this.props.curblr.data);
  const features = renderCurblrData(
      dt_to_set,
      this.state.day,
      this.state.time,
      this.state.mode
    );

  // takes CurbLR feed (loaded into map as a prop, above) and puts it into a "dataUri" that can be downloaded from the export button. (Linking to file pathway doesn't work bc of umi build... couldn't find a static location for the data)
    let curblrStr = JSON.stringify(this.props.curblr.data);
    let curblrDataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(curblrStr);

    const ACTIVITY_LENGTH_CALC = {
      "no standing": features.features
        .filter(f => f.properties.activity === "no standing")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0),
      "no parking": features.features
        .filter(f => f.properties.activity === "no parking")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0),
      "passenger loading": features.features
        .filter(f => f.properties.activity === "passenger loading")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0),
      "loading": features.features
        .filter(f => f.properties.activity === "loading")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0),
      "free parking": features.features
        .filter(f => f.properties.activity === "free parking")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0),
      "transit": features.features
        .filter(f => f.properties.activity === "transit")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0),
      "paid parking": features.features
        .filter(f => f.properties.activity === "paid parking")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0),
      "restricted": features.features
        .filter(f => f.properties.activity === "restricted")
        .map(f => f.properties.length)
        .reduce((acc, x) => acc + x, 0)
    };

    const MAXSTAY_LENGTH_CALC = {
      "3": features.features
        .filter(f => Number(f.properties.maxStay) <= 5)
        .map(f => Number(f.properties.length))
        .reduce((acc, x) => acc + x, 0),
      "15": features.features
        .filter(f => Number(f.properties.maxStay) === 15)
        .map(f => Number(f.properties.length))
        .reduce((acc, x) => acc + x, 0),
      "30": features.features
        .filter(f => Number(f.properties.maxStay) === 30)
        .map(f => Number(f.properties.length))
        .reduce((acc, x) => acc + x, 0),
      //"45": features.features.filter(f => f.properties.maxStay === '45').map(f => f.properties.length).reduce((acc, x) => acc + x, 0),
      "60": features.features
        .filter(f => Number(f.properties.maxStay) === 60)
        .map(f => Number(f.properties.length))
        .reduce((acc, x) => acc + x, 0),
      //"90": features.features.filter(f => f.properties.maxStay === '90').map(f => f.properties.length).reduce((acc, x) => acc + x, 0),
      "120": features.features
        .filter(f => Number(f.properties.maxStay) === 120)
        .map(f => Number(f.properties.length))
        .reduce((acc, x) => acc + x, 0),
      "180": features.features
        .filter(f => Number(f.properties.maxStay) === 180)
        .map(f => Number(f.properties.length))
        .reduce((acc, x) => acc + x, 0),
      "240": features.features
        .filter(f => Number(f.properties.maxStay) >= 240)
        .map(f => Number(f.properties.length))
        .reduce((acc, x) => acc + x, 0)
      //  "360": features.features.filter(f => f.properties.maxStay === '360').map(f => f.properties.length).reduce((acc, x) => acc + x, 0),
      //  "480": features.features.filter(f => f.properties.maxStay === '480').map(f => f.properties.length).reduce((acc, x) => acc + x, 0),
    };

    const activityPieData = [
      {
        x: "No Stopping",
        y: ACTIVITY_LENGTH_CALC["no standing"]
      },
      {
        x: "No Parking",
        y: ACTIVITY_LENGTH_CALC["no parking"]
      },
      {
        x: "Taxi, TNC, Other PUDO",
        y: ACTIVITY_LENGTH_CALC["passenger loading"]
      },
      {
        x: "Loading",
        y: ACTIVITY_LENGTH_CALC["loading"]
      },
      {
        x: "Transit",
        y: ACTIVITY_LENGTH_CALC["transit"]
      },
      {
        x: "Free Parking",
        y: ACTIVITY_LENGTH_CALC["free parking"]
      },
      {
        x: "Paid Parking",
        y: ACTIVITY_LENGTH_CALC["paid parking"]
      },
      {
        x: "Other Restricted Uses",
        y: ACTIVITY_LENGTH_CALC["restricted"]
      }
    ];

    const maxStayPieData = [
      {
        x: "5 min or less",
        y: MAXSTAY_LENGTH_CALC["3"]
      },
      {
        x: "15 min",
        y: MAXSTAY_LENGTH_CALC["15"]
      },
      {
        x: "30 min",
        y: MAXSTAY_LENGTH_CALC["30"]
      },
      // {
      //   x: '45 min',
      //   y: MAXSTAY_LENGTH_CALC['45'],
      // },
      {
        x: "1 hr",
        y: MAXSTAY_LENGTH_CALC["60"]
      },
      // {
      //   x: '90 min',
      //   y: MAXSTAY_LENGTH_CALC['90'],
      // },
      {
        x: "2 hr",
        y: MAXSTAY_LENGTH_CALC["120"]
      },
      {
        x: "3 hr",
        y: MAXSTAY_LENGTH_CALC["180"]
      },
      {
        x: "4 hr or more",
        y: MAXSTAY_LENGTH_CALC["240"]
      }
    ];
   
    const arrondissements_montreal = [
      { label: "plaza", value: "plaza"},
      { label: "Outremont", value: "Outremont"},
      // { label: "LaSalle", value: "LaSalle"},
      // { label: "Mont-Royal", value: "Mont-Royal"},
      { label: "Ville-Marie", value: "Ville-Marie"},
      { label: "Le Plateau-Mont-Royal", value: "Le Plateau-Mont-Royal"},
      // { label: "Hampstead", value: "Hampstead"},
      { label: "Le Sud-Ouest", value: "Le Sud-Ouest"},
      // { label: "Rivière-des-Prairies-Pointe-aux-Trembles", value: "Rivière-des-Prairies-Pointe-aux-Trembles"},
      { label: "Lachine", value: "Lachine"},
      // { label: "Dorval", value: "Dorval"},
      // { label: "Montréal-Nord", value: "Montréal-Nord"},
      // { label: "L'Île-Bizard-Sainte-Geneviève", value: "L'Île-Bizard-Sainte-Geneviève"},
      // { label: "Kirkland", value: "Kirkland"},
      // { label: "Dollard-des-Ormeaux", value: "Dollard-des-Ormeaux"},
      // { label: "Senneville", value: "Senneville"},
      { label: "Ahuntsic-Cartierville", value: "Ahuntsic-Cartierville"},
      // { label: "Côte-Saint-Luc", value: "Côte-Saint-Luc"},
      // { label: "Saint-Léonard", value: "Saint-Léonard"},
      // { label: "Montréal-Ouest", value: "Montréal-Ouest"},
      // { label: "Pointe-Claire", value: "Pointe-Claire"},
      // { label: "L'Île-Dorval", value: "L'Île-Dorval"},
      { label: "Mercier-Hochelaga-Maisonneuve", value: "Mercier-Hochelaga-Maisonneuve"},
      { label: "Côte-des-Neiges-Notre-Dame-de-Grâce", value: "Côte-des-Neiges-Notre-Dame-de-Grâce"},
      { label: "Rosemont-La Petite-Patrie", value: "Rosemont-La Petite-Patrie"},
      { label: "Saint-Laurent", value: "Saint-Laurent"},
      // { label: "Beaconsfield", value: "Beaconsfield"},
      { label: "Villeray-Saint-Michel-Parc-Extension", value: "Villeray-Saint-Michel-Parc-Extension"},
      // { label: "Westmount", value: "Westmount"},
      // { label: "Montréal-Est", value: "Montréal-Est"},
      // { label: "Anjou", value: "Anjou"},
      // { label: "Pierrefonds-Roxboro", value: "Pierrefonds-Roxboro"},
      // { label: "Sainte-Anne-de-Bellevue", value: "Sainte-Anne-de-Bellevue"},
      { label: "Verdun", value: "Verdun"},
      // { label: "Baie-d'Urfé", value: "Baie-d'Urfé"},
    ];


    return (
      <Layout>
        <button onClick={() => this.hideComponent("showHideCard")}>
                Hide/Show Menu
              </button>

        <Content>
          <MapGL
            ref={this._mapRef}
            mapboxApiAccessToken={mapboxAccessToken}
            mapStyle={mapStyle}
            {...viewport}
            onViewportChange={viewport => this.setState({ viewport })}
          />
        </Content>
        {showHideCard && (
          <Card
          size="small"
          title="Stationnements Montréal et Québec, QC"
          bordered={true}
          style={{
            position: "fixed",
            top: "40px",
            left: "40px",
            width: "350px",
            height: "auto",
            maxHeight: "100vh",
            overflow: "auto"
          }}
        >
          <br />
          &nbsp; &nbsp;Arrondissement/quartier à afficher:{" "}
          <Select onChange={this.changeGeoData} 
          style={{
            // position: "fixed",
            // top: "40px",
            // left: "40px",
            width: "275px"
          }}>
            {React.Children.toArray(geoDataFiles.map((f) =>
              <Select.Option value={f.path}>
                {f.label}
              </Select.Option>
            ))}
          </Select>
          <br />
          <br />
          &nbsp; &nbsp;Day:{" "}
          <Select defaultValue={day} onChange={this.changeDay}>
            <Select.Option value="mo">Monday</Select.Option>
            <Select.Option value="tu">Tuesday</Select.Option>
            <Select.Option value="we">Wednesday</Select.Option>
            <Select.Option value="th">Thursday</Select.Option>
            <Select.Option value="fr">Friday</Select.Option>
            <Select.Option value="sa">Saturday</Select.Option>
            <Select.Option value="su">Sunday</Select.Option>
          </Select>
          &nbsp; &nbsp;Time:{" "}
          <Select defaultValue={time} onChange={this.changeTime}
          style={{
            // position: "fixed",
            // top: "40px",
            // left: "40px",
            width: "85px"
          }}>
            <Select.Option value="00:01">00:00</Select.Option>
            <Select.Option value="01:01">01:00</Select.Option>
            <Select.Option value="02:01">02:00</Select.Option>
            <Select.Option value="03:01">03:00</Select.Option>
            <Select.Option value="04:01">04:00</Select.Option>
            <Select.Option value="05:01">05:00</Select.Option>
            <Select.Option value="06:01">06:00</Select.Option>
            <Select.Option value="07:01">07:00</Select.Option>
            <Select.Option value="08:01">08:00</Select.Option>
            <Select.Option value="09:01">09:00</Select.Option>
            <Select.Option value="10:01">10:00</Select.Option>
            <Select.Option value="11:01">11:00</Select.Option>
            <Select.Option value="12:01">12:00</Select.Option>
            <Select.Option value="13:01">13:00</Select.Option>
            <Select.Option value="14:01">14:00</Select.Option>
            <Select.Option value="15:01">15:00</Select.Option>
            <Select.Option value="16:01">16:00</Select.Option>
            <Select.Option value="17:01">17:00</Select.Option>
            <Select.Option value="18:01">18:00</Select.Option>
            <Select.Option value="19:01">19:00</Select.Option>
            <Select.Option value="20:01">20:00</Select.Option>
            <Select.Option value="21:01">21:00</Select.Option>
            <Select.Option value="22:01">22:00</Select.Option>
            <Select.Option value="23:01">23:00</Select.Option>
          </Select>
          <br />
          <br />
          &nbsp; &nbsp;View by:{" "}
          <Radio.Group
            defaultValue={mode}
            buttonStyle="solid"
            position="center"
            onChange={this.changeMode}
          >
            <Radio.Button value="activity">Activity</Radio.Button>
            <Radio.Button value="maxStay">Max Stay</Radio.Button>
          </Radio.Group>
          <br />
          <br />
          {mode === "maxStay" ? (
            <Pie
              animate={false}
              colors={Object.values(MAXSTAY_COLOR_MAP)}
              hasLegend
              title="Maximum Stay"
              subTitle={
                <>
                  Total car
                  <br />
                  lengths
                </>
              }
              total={() => (
                <>
                  <span>
                    {(
                      maxStayPieData.reduce((pre, now) => now.y + pre, 0) /
                      avgParkingLength
                    ).toLocaleString("en", {
                      style: "decimal",
                      maximumFractionDigits: 0,
                      minimumFractionDigits: 0
                    })}
                  </span>
                </>
              )}
              data={maxStayPieData}
              valueFormat={val => (
                <span>
                  {(val / avgParkingLength).toLocaleString("en", {
                    style: "decimal",
                    maximumFractionDigits: 0,
                    minimumFractionDigits: 0
                  })}{" "}
                  cars
                </span>
              )}
              height={240}
            />
          ) : (
            <Pie
              animate={false}
              colors={Object.values(ACTIVITY_COLOR_MAP)}
              hasLegend
              title="Activities"
              subTitle={
                <>
                  Total car
                  <br />
                  lengths
                </>
              }
              total={() => (
                <>
                  <span>
                    {(
                      activityPieData.reduce((pre, now) => now.y + pre, 0) /
                      avgParkingLength
                    ).toLocaleString("en", {
                      style: "decimal",
                      maximumFractionDigits: 0,
                      minimumFractionDigits: 0
                    })}
                  </span>
                </>
              )}
              data={activityPieData}
              valueFormat={val => (
                <span>
                  {(val / avgParkingLength).toLocaleString("en", {
                    style: "decimal",
                    maximumFractionDigits: 0,
                    minimumFractionDigits: 0
                  })}{" "}
                  cars
                </span>
              )}
              height={240}
            />
          )}
          <br />
          <Button type="primary" icon="download" block href={curblrDataUri} download="export.curblr.json">
                    Download CurbLR data
          </Button>
          <br />
          <br />
          <p style={{ "font-size": "11px" }}>
            Données de stationnements des villes <a href= "https://donnees.montreal.ca/ville-de-montreal/stationnement-sur-rue-signalisation-courant"> de Montréal </a> et de 
            <a href= "https://www.donneesquebec.ca/recherche/fr/dataset/vque_7"> de Québec </a>
          </p>
        </Card>
        )}
        {showHideCard && (
          <Card
          size="small"
          title="Filter"
          bordered={true}
          style={{
            position: "fixed",
            top: "40px",
            right: "40px",
            width: "auto",
            height: "auto",
            maxHeight: "100vh",
            overflow: "auto"
          }}
          >
          
          <div>
          <label for="sl_arrondissement">Arrondissement: </label>
            <select id ="sl_arrondissement"

            // onChange={this.setArrond}
            onChange={(event) => this.handleChange("sl_arrondRef", event)}
            >
            {arrondissements_montreal.map((option) => (
              <option value={option.value}>{option.label}</option>
            ))}
          </select>
          </div>
          <div>
          <label for="dt_picker"
          style={{
            textAlign: "justify",
          }}>
          Date et heure: </label>
            <DateTimePickerComponent placeholder="Choose a date and time"
              value={set_dateTimeRef}
              // min={minDate}
              // max={maxDate}
              id = "dt_picker"
              format="dd-MMM-yy HH:mm"
              step={15}
              onChange={(event) => this.handleChange("set_dateTimeRef", event)}>

              </DateTimePickerComponent>
          </div>
          <div>
            <Button type="primary" icon="search" onClick={this.sendRequest}>
              Filtrer
            </Button>
          </div>
        </Card>
        )}

        <Button
          size="small"
          type="primary" 
          href="https://wiki.lafabriquedesmobilites.fr/wiki/Carte_CurbLR_de_Montr%C3%A9al"
          style={{
            position: "fixed",
            bottom: "40px",
            right: "40px"
          }}
        >
            Plus d'informations sur la carte ici
        </Button>
      </Layout>
    );
  }
}

export default connect(mapStateToProps)(Map);
