TL;DR
=====

There are totally 3 types of hit object. (2018 Jan 27) Circle, Slide and Spin. In the format, it combines both `voice effect` and `position description`.

**Note: `hitobject_parser.py` in this package won't return 100% same results as the json shown in the below documents. Please reference to `hitobject_type.py` to get the return format.**

General Explanation
===================

**Map**

- up-left: `0,0`
- up-right: `512,0`
- down-left: `0,384`
- down-right: `512,384`
- center: `256,192`

* Note: only slide body can put outside of map(x<0 or x>512 or y<0 or y>384)

**Sampleset/Additions**

- auto: 0
- normal: 1
- soft: 2
- drum: 3

**Voice Effect**

- default: 0
- whilstle: 2
- finish: 4
- clap: 8
- whilstle + finish: 6(2+4)
- whilstle + clap: 10(2+8)
- finish + clap: 12(4+8)
- whilstle + finish + clap: 14(2+4+8)

* Note: a spin can also use voice_effect
* Note: a slide can use up to 3 voice_effect for start, body, end

**Point Type**
- normal circle: 1
- starting circle: 5
- normal slide: 2
- starting slide: 6
- spin: 12

* Note: first point of entire map must be "normal" type
* Note: the point after spin must be "starting" type
* Note: the point after long breaktime must be "starting" type

* Example:
    
    1 2 3 - 4 5 - 6~6 7~7
    1 1 1   5 1   6   2

    1 - {BREAK} - 2 3 4 5
    1             5 1 1 1

    1 -{S-P-I-N}- 2 3 4 5
    1  12         5 1 1 1

    1~~~1 2~2 - 3~~~3 4~4
    2     2     6     2


**Slide Type**
- straight: `L`
- curve: `P`
- cross: `B`

* Note: Cross means between start point and end point, there are other objects inside.


**Tick**
- one unit, SliderMultiplier:1: 100
- two unit, SliderMultiplier:1: 200
- one unit, SliderMultiplier:1.5: 150
- two unit, SliderMultiplier:1.5: 300
- one unit, SliderMultiplier:2: 200
- two unit, SliderMultiplier:2: 400

* Note: tick is a unit for evaluating the length of slide.
* Note: SliderMultiplier will impact the length of tick.
* Note: if length of slide is not enough, it will become a loop slide.

* 4 unit, SliderMultiplier:1: 3 points between start and end point
* 4 unit, SliderMultiplier:2: 7 points between start and end point
* 4 unit, SliderMultiplier:3: 11 points between start and end point

* Note: SliderMultiplier won't impact the length of tick, but the number of point inside slide. In game, player only need to hover on point to get the score of a slide.


Circle
======

**Format**

    Position:   x,y,timestamp,point_type,voice_effect
    Voice:      sampleset:additions:unknown_1:unknown_2:

**Example**

```python
# 256,192,3050,1,14
{
    "pos": (256,192)
    "timestamp": 3050,
    "point_type": 1,
    "voice_effect": 14,
}

# 256,192,3050,1,14,1:2:0:0:
{
    "pos": (256,192)
    "timestamp": 3050,
    "point_type": 1,
    "voice_effect": 14,
    "sampleset": 1,
    "additions": 2,
    "unknown_1": 0,
    "unknown_2": 0,
}
```


Slide
=====

Slide has 3 types, L(straight), P(curve), B(cross).

**General Format**

    Position:   start_x,start_y,timestamp,point_type,body_voice_effect,
                slide_type|x_1,y_1|x_2,y_2|...|end_x, end_y,unknown_1,tick,
    Voice:      start_voice_effect|end_voice_effect
                start_sampleset:start_additions|end_sampleset:end_additions,
                body_sampleset:body_additions:unknown_2:unknown_3

**Example**

```python
# Straight
# 256,192,4370,2,0,L|512:192,1,247.5
{
    "start_pos": (256,192),
    "timestamp": 4370,
    "point_type": 2,
    "body_voice_effect": 0,
    "slide_type": "L",
    "end_pos": (512,192),
    "unknown_1": 1,
    "tick": 247.5,
}

# Straight with Voice
# 0,192,350,2,8,L|368:192,1,360,2|4,1:2|3:1,2:3:0:0:
{
    "start_pos": (0,192),
    "timestamp": 350,
    "point_type": 2,
    "body_voice_effect": 8,
    "slide_type": "L",
    "end_pos": (368,192),
    "unknown_1": 1,
    "tick": 360,
    "start_voice_effect": 2,
    "end_voice_effect": 4,
    "start_sampleset":1
    "start_additions":2
    "end_sampleset":3
    "end_additions":1
    "body_sampleset":2
    "body_additions":3
    "unknown_2":0
    "unknown_3":0
}

# Loop Straight (Not visible from description)
# 56,192,350,2,0,L|304:192,1,45
{
    "start_pos": (56,192),
    "timestamp": 350,
    "point_type": 2,
    "body_voice_effect": 0,
    "slide_type": "L",
    "end_pos": (304,192),
    "unknown_1": 1,
    "tick": 45,
}

# Curve
# 247,72,7772,6,4,P|383:124|423:100|511:72,1,270
{
    "start_pos": (247,72),
    "timestamp": 7772,
    "point_type": 6,
    "body_voice_effect": 4,
    "slide_type": "P",
    "body_pos": [(383:124),(423:100)],
    "end_pos": (511,72),
    "unknown_1": 1,
    "tick": 270,
}

# Cross
# 152,180,891,2,0,B|184:204|92:128|116:84,1,112.5
{
    "start_pos": (152,180),
    "timestamp": 891,
    "point_type": 2,
    "body_voice_effect": 0,
    "slide_type": "B",
    "body_pos": [(184:204),(92:128)],
    "end_pos": (116,84),
    "unknown_1": 1,
    "tick": 112.5,
}
```

Spin
====

**General Format**

    Position:   256,192,start_timestamp,point_type,voice_effect,end_timestamp,
    Voice:      sampleset:additions:unknown_1:unknown_2:

    * position is fixed to (256,192)

**Example**

```python
# 256,192,2800,12,14,3250,1:2:0:0:
{
    "start_timestamp": 2800,
    "point_type": 12,
    "voice_effect": 14,
    "end_timestamp": 3250,
    "sampleset": 1,
    "additions": 2,
}
```
