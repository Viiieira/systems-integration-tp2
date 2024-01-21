import {Avatar, List, ListItem, ListItemIcon, ListItemText} from "@mui/material";
import LocationCityIcon from '@mui/icons-material/LocationCity';
import PictureInPictureAltIcon from '@mui/icons-material/PictureInPictureAlt';
import ContactsIcon from '@mui/icons-material/Contacts';
import React from "react";
import {Marker, Popup} from 'react-leaflet';
import {icon as leafletIcon, point} from "leaflet";

const LIST_PROPERTIES = [
    {"key": "province", label: "Province", Icon: LocationCityIcon},
    {"key": "salary", label: "Salary", Icon: ContactsIcon},
    {"key": "overall", label: "Overall", Icon: PictureInPictureAltIcon}
];

export function ObjectMarker({geoJSON}) {
    const properties = geoJSON?.properties;
    const {id, imgUrl, name} = properties;
    const coordinates = geoJSON?.geometry?.coordinates;

    return (
        <Marker
            position={coordinates}
            icon={leafletIcon({
                iconUrl: imgUrl,
                iconRetinaUrl: imgUrl,
                iconSize: point(50, 50),
            })}
        >
            <Popup>
                <List dense={true}>
                    <ListItem>
                        <ListItemIcon>
                            <Avatar alt={name} src={imgUrl}/>
                        </ListItemIcon>
                        <ListItemText primary={name}/>
                    </ListItem>
                    {LIST_PROPERTIES.map((property) => (
                        <ListItem key={property.key}>
                            <ListItemIcon>
                                <property.Icon style={{color: "black"}}/>
                            </ListItemIcon>
                            <ListItemText
                                primary={<span>
                                    {name} - {coordinates[0]}, {coordinates[1]}<br/>
                                    <label style={{fontSize: "xx-small"}}>({property.label} - Coordinates)</label>
                                </span>}
                            />
                        </ListItem>
                    ))}
                </List>
            </Popup>
        </Marker>
    );
}
