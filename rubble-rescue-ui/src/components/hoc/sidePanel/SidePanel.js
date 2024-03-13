import React from "react";
import {DATA} from '../../../data';
import { LEGEND_ITEMS } from "../../legend/legendItems";
import VictimListItem from "../../victimList/VictimListItem";
import LegendItem from "../../legend/LegendItem";
import Header from "../../header/PanelHeader";
import classes from './SidePanel.module.css';

const SidePanel = (props) => {
    return (
        <div className={classes.SidePanel}>
            <div className={classes.PanelSection}>
                <Header title={"Locations"} />
                {DATA.map((victim) => 
                    <VictimListItem
                        {...victim}
                        onDelete={e => props.onDelete(e, victim)}
                        onSelect={() => props.onSelect(victim)}
                        selectedVictim={props.selectedVictim}
                        key={victim.victimId}
                    />
                )}
            </div>
            <div className={classes.PanelSection}>
                <Header title={"Legend"} />
                {LEGEND_ITEMS.map((item) => <LegendItem {...item} key={item.src} />)}
            </div>
        </div>
    );
}

export default SidePanel;
