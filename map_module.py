import folium
from folium import plugins


def create_antarctic_map(
    ship_location=(-69.0, 39.0),
    destination_location=(-77.85, 166.67)
):
    """
    ANTARCTIC AI — RESEARCH VESSEL COMMAND CENTER
    M2 — Map + Visualization

    Current stage:
    Final rectangular command-center visualization.
    """

    # ============================================================
    # 1. BASE MAP
    # ============================================================

    antarctic_map = folium.Map(
        location=(-72, 100),
        zoom_start=2,
        min_zoom=2,
        max_zoom=8,
        tiles=(
            "https://server.arcgisonline.com/"
            "ArcGIS/rest/services/World_Imagery/"
            "MapServer/tile/{z}/{y}/{x}"
        ),
        attr="Esri World Imagery",
        control_scale=True,
        prefer_canvas=True
    )

    # ============================================================
    # 2. COMMAND CENTER TITLE
    # ============================================================

    title_html = """
    <div style="
        position: fixed;
        top: 10px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 9999;
        width: 620px;
        background: rgba(5, 12, 24, 0.94);
        border: 1px solid #4da6ff;
        border-radius: 12px;
        padding: 12px 20px;
        text-align: center;
        color: white;
        font-family: Arial, sans-serif;
        box-shadow: 0 0 18px rgba(0,150,255,0.35);
    ">
        <div style="
            font-size: 23px;
            font-weight: bold;
            letter-spacing: 2px;
        ">
            ANTARCTIC AI
        </div>

        <div style="
            font-size: 14px;
            margin-top: 4px;
            color: #9fd7ff;
            letter-spacing: 1px;
        ">
            RESEARCH VESSEL COMMAND CENTER
        </div>

        <div style="
            margin-top: 7px;
            font-size: 11px;
            color: #7cff9b;
        ">
            ● SYSTEM ONLINE &nbsp;&nbsp; | &nbsp;&nbsp;
            AI NAVIGATION ACTIVE
        </div>
    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(title_html)
    )

    # ============================================================
    # 3. VESSEL
    # ============================================================

    vessel_group = folium.FeatureGroup(
        name="🚢 Research Vessel"
    )

    folium.Marker(
        location=ship_location,
        tooltip="YOUR RESEARCH VESSEL",
        popup="""
        <b>Research Vessel</b><br>
        Speed: 12 knots<br>
        Status: Navigation Active
        """,
        icon=folium.Icon(
            color="blue",
            icon="ship",
            prefix="fa"
        )
    ).add_to(vessel_group)

    folium.Marker(
        location=(ship_location[0] + 1.8, ship_location[1]),
        icon=folium.DivIcon(
            html="""
            <div style="
                font-size:12px;
                font-weight:bold;
                color:white;
                background:rgba(0,60,120,0.85);
                padding:4px 7px;
                border-radius:5px;
                border:1px solid #4da6ff;
                white-space:nowrap;
            ">
                🚢 YOUR VESSEL
            </div>
            """
        )
    ).add_to(vessel_group)

    vessel_group.add_to(antarctic_map)

    # ============================================================
    # 4. DESTINATION
    # ============================================================

    destination_group = folium.FeatureGroup(
        name="📍 Mission Destination"
    )

    folium.Marker(
        location=destination_location,
        tooltip="MISSION DESTINATION",
        popup="""
        <b>Mission Destination</b><br>
        Antarctic Research Station
        """,
        icon=folium.Icon(
            color="red",
            icon="flag",
            prefix="fa"
        )
    ).add_to(destination_group)

    folium.Marker(
        location=(
            destination_location[0] + 1.8,
            destination_location[1]
        ),
        icon=folium.DivIcon(
            html="""
            <div style="
                font-size:12px;
                font-weight:bold;
                color:white;
                background:rgba(120,20,20,0.9);
                padding:4px 7px;
                border-radius:5px;
                border:1px solid #ff6666;
                white-space:nowrap;
            ">
                📍 MISSION DESTINATION
            </div>
            """
        )
    ).add_to(destination_group)

    destination_group.add_to(antarctic_map)

    # ============================================================
    # 5. SEA-ICE CONDITIONS — CLEAN VISUALIZATION
    # ============================================================

    ice_group = folium.FeatureGroup(
        name="🧊 Sea-Ice Conditions"
    )

    # ------------------------------------------------------------
    # LOW ICE
    # ------------------------------------------------------------

    low_ice = [
        (-64.5, 40),
        (-65.5, 60),
        (-66.5, 82),
        (-68.0, 105),
        (-70.0, 128),
        (-72.5, 150),
        (-75.0, 165),
        (-78.0, 168),
        (-77.0, 145),
        (-75.0, 120),
        (-72.5, 95),
        (-70.0, 70),
        (-67.0, 48)
    ]

    folium.Polygon(
        locations=low_ice,
        color="#65d6ff",
        weight=2,
        fill=True,
        fill_color="#65d6ff",
        fill_opacity=0.08,
        tooltip="🧊 LOW ICE — Lower Concentration",
        popup="""
        <b>LOW SEA-ICE</b><br>
        Lower ice concentration<br>
        Navigation conditions: Relatively open
        """
    ).add_to(ice_group)

    # ------------------------------------------------------------
    # MEDIUM ICE
    # ------------------------------------------------------------

    medium_ice = [
        (-68.0, 52),
        (-69.0, 72),
        (-71.0, 94),
        (-73.0, 116),
        (-75.0, 138),
        (-77.0, 155),
        (-80.0, 162),
        (-81.5, 142),
        (-80.0, 118),
        (-77.5, 94),
        (-74.5, 72),
        (-71.5, 55)
    ]

    folium.Polygon(
        locations=medium_ice,
        color="#ffc107",
        weight=2,
        fill=True,
        fill_color="#ffc107",
        fill_opacity=0.10,
        tooltip="🧊 MEDIUM ICE — Moderate Concentration",
        popup="""
        <b>MEDIUM SEA-ICE</b><br>
        Moderate ice concentration<br>
        Navigation conditions: Caution required
        """
    ).add_to(ice_group)

    # ------------------------------------------------------------
    # HIGH ICE
    # ------------------------------------------------------------

    high_ice = [
        (-73.0, 68),
        (-75.0, 86),
        (-77.0, 105),
        (-79.0, 125),
        (-81.0, 143),
        (-84.0, 151),
        (-85.0, 132),
        (-84.0, 108),
        (-82.0, 88),
        (-78.5, 72)
    ]

    folium.Polygon(
        locations=high_ice,
        color="#ff4d4d",
        weight=2,
        fill=True,
        fill_color="#ff4d4d",
        fill_opacity=0.12,
        tooltip="⚠ HIGH ICE — High Concentration",
        popup="""
        <b>HIGH SEA-ICE</b><br>
        High ice concentration<br>
        Navigation conditions: Difficult
        """
    ).add_to(ice_group)

    # ------------------------------------------------------------
    # ICE CONDITION LABELS
    # ------------------------------------------------------------

    folium.Marker(
        location=(-67.5, 95),
        icon=folium.DivIcon(
            html="""
            <div style="
                color:#65d6ff;
                font-size:11px;
                font-weight:bold;
                background:rgba(0,20,35,0.75);
                padding:3px 6px;
                border:1px solid #65d6ff;
                border-radius:4px;
                white-space:nowrap;
            ">
                LOW ICE
            </div>
            """
        )
    ).add_to(ice_group)

    folium.Marker(
        location=(-75.5, 118),
        icon=folium.DivIcon(
            html="""
            <div style="
                color:#ffc107;
                font-size:11px;
                font-weight:bold;
                background:rgba(35,25,0,0.75);
                padding:3px 6px;
                border:1px solid #ffc107;
                border-radius:4px;
                white-space:nowrap;
            ">
                MEDIUM ICE
            </div>
            """
        )
    ).add_to(ice_group)

    folium.Marker(
        location=(-80.0, 115),
        icon=folium.DivIcon(
            html="""
            <div style="
                color:#ff6666;
                font-size:11px;
                font-weight:bold;
                background:rgba(45,0,0,0.78);
                padding:3px 6px;
                border:1px solid #ff4d4d;
                border-radius:4px;
                white-space:nowrap;
            ">
                ⚠ HIGH ICE
            </div>
            """
        )
    ).add_to(ice_group)

    # ------------------------------------------------------------
    # ADD SEA-ICE GROUP TO MAP
    # ------------------------------------------------------------

    ice_group.add_to(antarctic_map)

    # ============================================================
    # 6. ROUTES — CLEAN NAVIGATION VISUALIZATION
    # ============================================================

    routes_group = folium.FeatureGroup(
        name="🛣️ Navigation Routes"
    )

    # ------------------------------------------------------------
    # ROUTE A — HIGHER RISK
    # ------------------------------------------------------------

    route_a = [
        ship_location,
        (-68.5, 50),
        (-69.0, 68),
        (-70.0, 88),
        (-71.5, 110),
        (-73.0, 132),
        (-75.0, 150),
        destination_location
    ]

    folium.PolyLine(
        route_a,
        color="#ff4d4d",
        weight=4,
        opacity=0.85,
        dash_array="2,5",
        tooltip="🔴 Route A — Higher Risk",
        popup="""
        <b>Route A</b><br>
        Risk Level: HIGH<br>
        Route Type: Higher Risk
        """
    ).add_to(routes_group)

    # ------------------------------------------------------------
    # ROUTE B — ALTERNATIVE
    # ------------------------------------------------------------

    route_b = [
        ship_location,
        (-70.0, 48),
        (-71.5, 65),
        (-73.0, 82),
        (-75.0, 103),
        (-76.0, 125),
        (-76.8, 148),
        destination_location
    ]

    folium.PolyLine(
        route_b,
        color="#ffb347",
        weight=4,
        opacity=0.9,
        dash_array="12,8",
        tooltip="🟠 Route B — Alternative",
        popup="""
        <b>Route B</b><br>
        Risk Level: MEDIUM<br>
        Route Type: Alternative
        """
    ).add_to(routes_group)

    # ------------------------------------------------------------
    # ROUTE C — RECOMMENDED
    # ------------------------------------------------------------

    route_c = [
        ship_location,
        (-67.5, 46),
        (-69.0, 60),
        (-70.0, 75),
        (-71.5, 94),
        (-73.0, 115),
        (-75.0, 137),
        (-76.5, 153),
        destination_location
    ]

    recommended_line = folium.PolyLine(
        route_c,
        color="#42ff7b",
        weight=7,
        opacity=1.0,
        tooltip="⭐ Route C — Recommended",
        popup="""
        <b>Route C — Recommended</b><br>
        Route Type: Recommended<br>
        Purpose: Safer + Fuel-Efficient Navigation
        """
    )

    recommended_line.add_to(routes_group)

    # ------------------------------------------------------------
    # ROUTE A LABEL
    # ------------------------------------------------------------

    folium.Marker(
        location=(-69.5, 72),
        icon=folium.DivIcon(
            html="""
            <div style="
                background:rgba(40,5,5,0.88);
                color:#ff6666;
                padding:4px 8px;
                border-radius:5px;
                border:1px solid #ff4d4d;
                font-size:11px;
                font-weight:bold;
                white-space:nowrap;
                box-shadow:0 0 5px rgba(255,0,0,0.4);
            ">
                🔴 ROUTE A
                <span style="
                    font-size:9px;
                    font-weight:normal;
                ">
                    HIGH RISK
                </span>
            </div>
            """
        )
    ).add_to(routes_group)

    # ------------------------------------------------------------
    # ROUTE B LABEL
    # ------------------------------------------------------------

    folium.Marker(
        location=(-73.5, 91),
        icon=folium.DivIcon(
            html="""
            <div style="
                background:rgba(45,25,5,0.88);
                color:#ffb347;
                padding:4px 8px;
                border-radius:5px;
                border:1px solid #ffb347;
                font-size:11px;
                font-weight:bold;
                white-space:nowrap;
                box-shadow:0 0 5px rgba(255,165,0,0.35);
            ">
                🟠 ROUTE B
                <span style="
                    font-size:9px;
                    font-weight:normal;
                ">
                    ALTERNATIVE
                </span>
            </div>
            """
        )
    ).add_to(routes_group)

    # ------------------------------------------------------------
    # ROUTE C LABEL
    # ------------------------------------------------------------

    folium.Marker(
        location=(-71.5, 94),
        icon=folium.DivIcon(
            html="""
            <div style="
                background:rgba(5,55,20,0.92);
                color:#42ff7b;
                padding:5px 9px;
                border-radius:6px;
                border:1px solid #42ff7b;
                font-size:12px;
                font-weight:bold;
                white-space:nowrap;
                box-shadow:0 0 8px rgba(66,255,123,0.45);
            ">
                ⭐ RECOMMENDED ROUTE
            </div>
            """
        )
    ).add_to(routes_group)

    # ------------------------------------------------------------
    # ROUTE GROUP
    # ------------------------------------------------------------

    routes_group.add_to(antarctic_map)

    # ============================================================
    # 7. ICEBERGS
    # ============================================================

    iceberg_group = folium.FeatureGroup(
        name="🧊 Icebergs"
    )

    iceberg_data = [
        ("ICEBERG 01", (-68.5, 55), "North-East"),
        ("ICEBERG 02", (-71.5, 78), "East"),
        ("ICEBERG 03", (-74.0, 105), "South-East")
    ]

    for name, location, direction in iceberg_data:

        folium.Marker(
            location=location,
            tooltip=name,
            popup=f"""
            <b>{name}</b><br>
            Direction: {direction}<br>
            Status: Being Tracked
            """,
            icon=folium.DivIcon(
                html="""
                <div style="
                    font-size:22px;
                    text-align:center;
                    filter:drop-shadow(0 0 4px black);
                ">
                    🧊
                </div>
                """
            )
        ).add_to(iceberg_group)

        folium.Marker(
            location=(location[0] + 1.2, location[1]),
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    color:white;
                    font-size:10px;
                    background:rgba(0,0,0,0.65);
                    padding:2px 5px;
                    border-radius:3px;
                    white-space:nowrap;
                ">
                    {name}
                </div>
                """
            )
        ).add_to(iceberg_group)

    iceberg_group.add_to(antarctic_map)

        # ============================================================
    # 8. ICEBERG PREDICTED TRAJECTORIES
    # ============================================================

    trajectory_group = folium.FeatureGroup(
        name="🔮 Predicted Iceberg Movement"
    )

    # ------------------------------------------------------------
    # DEMO PREDICTION PATHS
    # ------------------------------------------------------------
    # Format:
    # Current Position → Predicted Points → Future Position

    iceberg_predictions = [
        {
            "name": "ICEBERG 01",
            "current": (-68.5, 55),
            "predicted": [
                (-67.8, 61),
                (-67.1, 67)
            ],
            "future": (-66.4, 73)
        },
        {
            "name": "ICEBERG 02",
            "current": (-71.5, 78),
            "predicted": [
                (-71.0, 85),
                (-70.5, 92)
            ],
            "future": (-70.0, 99)
        },
        {
            "name": "ICEBERG 03",
            "current": (-74.0, 105),
            "predicted": [
                (-74.5, 112),
                (-75.0, 119)
            ],
            "future": (-75.5, 126)
        }
    ]

    # ------------------------------------------------------------
    # DRAW EACH ICEBERG PREDICTION
    # ------------------------------------------------------------

    for iceberg in iceberg_predictions:

        current = iceberg["current"]
        predicted = iceberg["predicted"]
        future = iceberg["future"]

        full_path = [current] + predicted + [future]

        # --------------------------------------------------------
        # PREDICTED TRAJECTORY LINE
        # --------------------------------------------------------

        trajectory_line = folium.PolyLine(
            full_path,
            color="#38d9ff",
            weight=3,
            opacity=0.9,
            dash_array="8,8",
            tooltip=f"🔮 {iceberg['name']} — Predicted Movement",
            popup=f"""
            <b>{iceberg['name']}</b><br>
            Current Position → Future Position<br>
            Prediction Status: ACTIVE
            """
        )

        trajectory_line.add_to(trajectory_group)

        # --------------------------------------------------------
        # PREDICTED POINTS
        # --------------------------------------------------------

        for point in predicted:

            folium.CircleMarker(
                location=point,
                radius=4,
                color="#38d9ff",
                fill=True,
                fill_color="#38d9ff",
                fill_opacity=0.9,
                tooltip="Predicted Position"
            ).add_to(trajectory_group)

        # --------------------------------------------------------
        # FUTURE POSITION
        # --------------------------------------------------------

        folium.Marker(
            location=future,
            tooltip=f"{iceberg['name']} — Future Position",
            popup=f"""
            <b>{iceberg['name']}</b><br>
            🔮 Predicted Future Position<br>
            Tracking Status: ACTIVE
            """,
            icon=folium.DivIcon(
                html="""
                <div style="
                    width:24px;
                    height:24px;
                    border:2px solid #38d9ff;
                    border-radius:50%;
                    background:rgba(0,40,60,0.85);
                    color:#38d9ff;
                    font-size:13px;
                    font-weight:bold;
                    text-align:center;
                    line-height:20px;
                    box-shadow:0 0 8px rgba(56,217,255,0.7);
                ">
                    ➜
                </div>
                """
            )
        ).add_to(trajectory_group)

        # --------------------------------------------------------
        # FUTURE POSITION LABEL
        # --------------------------------------------------------

        folium.Marker(
            location=(future[0] + 1.0, future[1]),
            icon=folium.DivIcon(
                html=f"""
                <div style="
                    color:#38d9ff;
                    background:rgba(0,20,35,0.82);
                    border:1px solid #38d9ff;
                    border-radius:4px;
                    padding:3px 6px;
                    font-size:10px;
                    font-weight:bold;
                    white-space:nowrap;
                ">
                    🔮 {iceberg['name']} FUTURE
                </div>
                """
            )
        ).add_to(trajectory_group)

    # ------------------------------------------------------------
    # PREDICTION LEGEND ON MAP
    # ------------------------------------------------------------

    folium.Marker(
        location=(-66.0, 82),
        icon=folium.DivIcon(
            html="""
            <div style="
                background:rgba(5,20,35,0.90);
                border:1px solid #38d9ff;
                border-radius:6px;
                padding:6px 9px;
                color:#38d9ff;
                font-family:Arial,sans-serif;
                font-size:10px;
                font-weight:bold;
                white-space:nowrap;
                box-shadow:0 0 8px rgba(56,217,255,0.35);
            ">
                🧊 CURRENT
                &nbsp;→&nbsp;
                🔮 PREDICTED
                &nbsp;→&nbsp;
                📍 FUTURE
            </div>
            """
        )
    ).add_to(trajectory_group)

    # ------------------------------------------------------------
    # ADD TRAJECTORY GROUP
    # ------------------------------------------------------------

    trajectory_group.add_to(antarctic_map)
    # ============================================================
    # 9. RISK ZONES
    # ============================================================

    risk_group = folium.FeatureGroup(
        name="⚠️ Risk Zones"
    )

    folium.Circle(
        location=(-71, 65),
        radius=180000,
        color="#ff3333",
        weight=2,
        fill=True,
        fill_color="#ff3333",
        fill_opacity=0.10,
        tooltip="HIGH RISK ZONE"
    ).add_to(risk_group)

    folium.Circle(
        location=(-74, 105),
        radius=140000,
        color="#ff9900",
        weight=2,
        fill=True,
        fill_color="#ff9900",
        fill_opacity=0.09,
        tooltip="MEDIUM RISK ZONE"
    ).add_to(risk_group)

    folium.Marker(
        location=(-70.5, 64),
        icon=folium.DivIcon(
            html="""
            <div style="
                color:#ff5555;
                font-weight:bold;
                font-size:12px;
            ">
                ⚠ HIGH RISK
            </div>
            """
        )
    ).add_to(risk_group)

    folium.Marker(
        location=(-73.5, 105),
        icon=folium.DivIcon(
            html="""
            <div style="
                color:#ffb347;
                font-weight:bold;
                font-size:12px;
            ">
                ⚠ MEDIUM RISK
            </div>
            """
        )
    ).add_to(risk_group)

    risk_group.add_to(antarctic_map)

    # ============================================================
    # 10. WEATHER / WIND
    # ============================================================

    weather_group = folium.FeatureGroup(
        name="🌬️ Weather / Wind"
    )

    wind_points = [
        (-66.5, 42),
        (-68.5, 60),
        (-71, 82),
        (-73.5, 105),
        (-76, 128)
    ]

    for location in wind_points:

        folium.Marker(
            location=location,
            icon=folium.DivIcon(
                html="""
                <div style="
                    font-size:18px;
                    color:#9fd7ff;
                    text-shadow:0 0 4px black;
                ">
                    ↗
                </div>
                """
            )
        ).add_to(weather_group)

    weather_group.add_to(antarctic_map)

    # ============================================================
    # 11. LEFT COMMAND PANEL
    # ============================================================

    left_panel = """
    <div style="
        position: fixed;
        left: 15px;
        top: 90px;
        z-index: 9998;
        width: 255px;
        background: rgba(5, 12, 24, 0.93);
        border: 1px solid #4da6ff;
        border-radius: 10px;
        padding: 14px;
        color: white;
        font-family: Arial, sans-serif;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    ">

        <div style="
            font-size:15px;
            font-weight:bold;
            color:#8fd3ff;
            border-bottom:1px solid #31506d;
            padding-bottom:8px;
            margin-bottom:10px;
        ">
            🚢 VESSEL STATUS
        </div>

        <div>Mission: <b>Antarctic Research</b></div>
        <div>Speed: <b>12 knots</b></div>
        <div>Status:
            <span style="color:#42ff7b;">
                ● NAVIGATION ACTIVE
            </span>
        </div>

        <div style="
            margin-top:12px;
            font-size:15px;
            font-weight:bold;
            color:#ff6666;
        ">
            ⚠ RISK STATUS
        </div>

        <div style="
            font-size:25px;
            font-weight:bold;
            color:#ff5555;
        ">
            HIGH
        </div>

        <div>Risk Score: <b>78 / 100</b></div>

        <div style="
            margin-top:12px;
            font-size:15px;
            font-weight:bold;
            color:#8fd3ff;
        ">
            🛣️ ROUTES
        </div>

        <div style="margin-top:5px;">
            <span style="color:#ff4d4d;">●</span>
            Route A — Higher Risk
        </div>

        <div>
            <span style="color:#ffb347;">●</span>
            Route B — Alternative
        </div>

        <div>
            <span style="color:#42ff7b;">●</span>
            Route C — Recommended
        </div>

    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(left_panel)
    )
    # ============================================================
    # 11.5 ROUTE COMPARISON PANEL
    # ============================================================

    route_comparison_panel = """
    <div style="
        position: fixed;
        left: 15px;
        top: 365px;
        z-index: 9998;
        width: 255px;
        background: rgba(5, 12, 24, 0.94);
        border: 1px solid #31506d;
        border-radius: 10px;
        padding: 12px 14px;
        color: white;
        font-family: Arial, sans-serif;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    ">

        <div style="
            font-size:15px;
            font-weight:bold;
            color:#8fd3ff;
            border-bottom:1px solid #31506d;
            padding-bottom:8px;
            margin-bottom:10px;
        ">
            🛣️ ROUTE COMPARISON
        </div>

        <!-- ROUTE A -->
        <div style="
            border-left:4px solid #ff4d4d;
            padding-left:8px;
            margin-bottom:9px;
        ">
            <b style="color:#ff6666;">🔴 ROUTE A</b><br>
            <span style="font-size:11px;">
                Risk: <b style="color:#ff6666;">HIGH</b>
                &nbsp; | &nbsp;
                Distance: <b>3800 km</b>
            </span>
        </div>

        <!-- ROUTE B -->
        <div style="
            border-left:4px solid #ffb347;
            padding-left:8px;
            margin-bottom:9px;
        ">
            <b style="color:#ffb347;">🟠 ROUTE B</b><br>
            <span style="font-size:11px;">
                Risk: <b style="color:#ffb347;">MEDIUM</b>
                &nbsp; | &nbsp;
                Distance: <b>3950 km</b>
            </span>
        </div>

        <!-- ROUTE C -->
        <div style="
            border-left:4px solid #42ff7b;
            padding-left:8px;
            margin-bottom:4px;
        ">
            <b style="color:#42ff7b;">⭐ ROUTE C</b><br>
            <span style="font-size:11px;">
                Risk: <b style="color:#42ff7b;">LOW</b>
                &nbsp; | &nbsp;
                Distance: <b>3900 km</b>
            </span>
        </div>

        <div style="
            margin-top:10px;
            padding-top:8px;
            border-top:1px solid #31506d;
            font-size:10px;
            color:#9fd7ff;
        ">
            ⭐ Recommended route based on
            safety + fuel efficiency
        </div>

    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(route_comparison_panel)
    )
        # ============================================================
    # 11.6 RECOMMENDED ROUTE DECISION PANEL
    # ============================================================

    recommended_route_panel = """
    <div style="
        position: fixed;
        right: 15px;
        top: 365px;
        z-index: 9998;
        width: 255px;
        background: rgba(5, 12, 24, 0.95);
        border: 1px solid #31506d;
        border-radius: 10px;
        padding: 12px 14px;
        color: white;
        font-family: Arial, sans-serif;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    ">

        <div style="
            font-size:15px;
            font-weight:bold;
            color:#8fd3ff;
            border-bottom:1px solid #31506d;
            padding-bottom:8px;
            margin-bottom:10px;
        ">
            ⭐ AI ROUTE DECISION
        </div>

        <div style="
            background: rgba(50, 255, 120, 0.08);
            border: 1px solid #42ff7b;
            border-radius: 7px;
            padding: 10px;
            margin-bottom:10px;
        ">
            <div style="
                font-size:14px;
                font-weight:bold;
                color:#42ff7b;
            ">
                ⭐ ROUTE C RECOMMENDED
            </div>

            <div style="
                font-size:11px;
                margin-top:7px;
                line-height:1.7;
            ">
                🛡️ Safety:
                <b style="color:#42ff7b;">LOW RISK</b><br>

                🛣️ Distance:
                <b>3900 km</b><br>

                ⛽ Fuel:
                <b>Efficient</b>
            </div>
        </div>

        <div style="
            font-size:11px;
            color:#b9c9d8;
            line-height:1.6;
        ">
            <b style="color:#8fd3ff;">AI Reason:</b><br>
            Route selected by comparing
            safety conditions and route efficiency.
        </div>

        <div style="
            margin-top:10px;
            padding-top:8px;
            border-top:1px solid #31506d;
            font-size:10px;
            color:#42ff7b;
            text-align:center;
        ">
            🤖 AI NAVIGATION ACTIVE
        </div>

    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(recommended_route_panel)
    )
        # ============================================================
    # 11.7 DYNAMIC RE-ROUTING
    # ============================================================

    reroute_group = folium.FeatureGroup(
        name="🔄 Dynamic Re-routing"
    )

    # Previous route — shown as a faint/dashed path
    previous_route = [
        ship_location,
        (-67.5, 46),
        (-69.0, 60),
        (-70.0, 75),
        (-71.5, 94),
        (-73.0, 115),
        (-75.0, 137),
        (-76.5, 153),
        destination_location
    ]

    folium.PolyLine(
        previous_route,
        color="#888888",
        weight=3,
        opacity=0.55,
        dash_array="6,10",
        tooltip="Previous Route"
    ).add_to(reroute_group)

    # New updated route
    updated_route = [
        ship_location,
        (-67.0, 45),
        (-68.0, 57),
        (-69.5, 70),
        (-70.5, 84),
        (-72.0, 100),
        (-73.5, 120),
        (-75.0, 142),
        (-76.5, 157),
        destination_location
    ]

    folium.PolyLine(
        updated_route,
        color="#42ff7b",
        weight=6,
        opacity=0.95,
        tooltip="AI Updated Safe Route"
    ).add_to(reroute_group)

    # Re-routing point
    folium.Marker(
        location=(-69.5, 70),
        tooltip="AI Re-routing Point",
        popup="AI detected a route change and updated the navigation path.",
        icon=folium.DivIcon(
            html="""
            <div style="
                font-size:22px;
                color:#42ff7b;
                text-shadow:0 0 8px black;
            ">🔄</div>
            """
        )
    ).add_to(reroute_group)

    reroute_group.add_to(antarctic_map)

    # Re-routing status panel
    reroute_status = """
    <div style="
        position: fixed;
        left: 50%;
        bottom: 70px;
        transform: translateX(-50%);
        z-index: 9998;
        background: rgba(5, 12, 24, 0.95);
        border: 1px solid #42ff7b;
        border-radius: 8px;
        padding: 9px 18px;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
        box-shadow: 0 0 12px rgba(0,0,0,0.5);
    ">
        <b style="color:#42ff7b;">
            🔄 ROUTE UPDATED
        </b>
        <br>
        <span style="font-size:10px;">
            AI Navigation • New path generated
        </span>
    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(reroute_status)
    )
    # ============================================================
    # 12. RIGHT STATUS PANEL
    # ============================================================

    right_panel = """
    <div style="
        position: fixed;
        right: 15px;
        top: 90px;
        z-index: 9998;
        width: 270px;
        background: rgba(5, 12, 24, 0.93);
        border: 1px solid #4da6ff;
        border-radius: 10px;
        padding: 14px;
        color: white;
        font-family: Arial, sans-serif;
        box-shadow: 0 0 15px rgba(0,0,0,0.5);
    ">

        <div style="
            font-size:15px;
            font-weight:bold;
            color:#8fd3ff;
            border-bottom:1px solid #31506d;
            padding-bottom:8px;
            margin-bottom:10px;
        ">
            📊 ENVIRONMENT
        </div>

        <div>Sea-Ice:
            <b style="color:#ffc107;">
                MEDIUM
            </b>
        </div>

        <div>Wind:
            <b>↗ 18 knots</b>
        </div>

        <div>Ocean Current:
            <b>1.8 knots</b>
        </div>

        <div style="
            margin-top:12px;
            font-size:15px;
            font-weight:bold;
            color:#38d9ff;
        ">
            🧊 ICEBERG TRACKING
        </div>

        <div>Tracked Icebergs:
            <b>03</b>
        </div>

        <div>Predicted Movement:
            <b style="color:#38d9ff;">
                ACTIVE
            </b>
        </div>

        <div style="
            margin-top:12px;
            font-size:15px;
            font-weight:bold;
            color:#42ff7b;
        ">
            🔄 ROUTE UPDATE
        </div>

        <div>
            AI monitoring route continuously.
        </div>

    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(right_panel)
    )

    # ============================================================
    # 13. BOTTOM COMMAND BAR
    # ============================================================

    bottom_panel = """
    <div style="
        position: fixed;
        left: 50%;
        bottom: 12px;
        transform: translateX(-50%);
        z-index: 9998;
        width: 760px;
        background: rgba(5, 12, 24, 0.94);
        border: 1px solid #31506d;
        border-radius: 10px;
        padding: 10px;
        color: white;
        font-family: Arial, sans-serif;
        text-align: center;
    ">

        <span style="margin:0 14px;">
            🧊 ICE
            <b style="color:#ffc107;">MEDIUM</b>
        </span>

        <span style="margin:0 14px;">
            🌬 WIND
            <b>18 kt</b>
        </span>

        <span style="margin:0 14px;">
            🌊 OCEAN
            <b>1.8 kt</b>
        </span>

        <span style="margin:0 14px;">
            🧊 ICEBERGS
            <b>03 TRACKED</b>
        </span>

        <span style="margin:0 14px;">
            🔄 AI
            <b style="color:#42ff7b;">ONLINE</b>
        </span>

    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(bottom_panel)
    )

    # ============================================================
    # 14. LEGEND
    # ============================================================

    legend_html = """
    <div style="
        position: fixed;
        right: 15px;
        bottom: 85px;
        z-index: 9998;
        width: 270px;
        background: rgba(5, 12, 24, 0.92);
        border: 1px solid #31506d;
        border-radius: 8px;
        padding: 10px;
        color: white;
        font-family: Arial, sans-serif;
        font-size: 12px;
    ">

        <b style="font-size:14px;">
            MAP LEGEND
        </b>

        <hr style="border-color:#31506d;">

        🚢 Vessel<br>
        📍 Mission Destination<br>
        🧊 Iceberg<br>
        <span style="color:#38d9ff;">- - -</span>
        Predicted Iceberg Movement<br>

        <span style="color:#42ff7b;">━━━━</span>
        Recommended Route<br>

        <span style="color:#ff4d4d;">━━━━</span>
        Higher Risk Route<br>

        <span style="color:#ffb347;">- - -</span>
        Alternative Route<br>

        <span style="color:#ff5555;">●</span>
        High Risk Zone<br>

        <span style="color:#ffc107;">●</span>
        Medium Risk Zone

    </div>
    """

    antarctic_map.get_root().html.add_child(
        folium.Element(legend_html)
    )

    # ============================================================
    # 15. LAYER CONTROL
    # ============================================================

    folium.LayerControl(
        collapsed=False,
        position="topleft"
    ).add_to(antarctic_map)

    # ============================================================
    # 16. MOUSE COORDINATES
    # ============================================================

    plugins.MousePosition(
        position="bottomleft",
        separator=" | ",
        prefix="Coordinates:",
        num_digits=3
    ).add_to(antarctic_map)

    # ============================================================
    # 17. FIT COMPLETE MISSION AREA
    # ============================================================

    all_locations = (
        route_a
        + route_b
        + route_c
        + [ship_location, destination_location]
        + [item[1] for item in iceberg_data]
    )

    antarctic_map.fit_bounds(
        all_locations,
        padding=(80, 80)
    )

    # ============================================================
    # 18. RETURN
    # ============================================================

    return antarctic_map