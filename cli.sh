#!/bin/bash

PY=python
PY_OPTS=-m
STITCHER_DIR=app.stitcher
UTILITY_DIR=app.util
FLEX_DIR=app.stitcher.flex
SNAPPER_DIR=app.snapper
PROFILE_DIR=app.profile

OPT_MSG="0) Quit\n\
1) Run stitcher\n\
2) Calibrate\n\
3) Flex\n\
4) See valid camera feeds\n\
5) Capture feeds\n\
6) Snap\n\
7) Profile stitcher"

RUN_PACKAGE="${PY} ${PY_OPTS}"

function read_opt() {
  echo ""
  echo -e "${OPT_MSG}"

  while ! [[ ${OPT} = 0 ]]
  do
    read -p "Choose option: " OPT
    case "${OPT}" in
      0)
        exit
        ;;
      1)
        stitch
        ;;
      2)
        calibrate
        ;;
      3)
        flex
        ;;
      4)
        validate
        ;;
      5)
        capture
        ;;
      6)
        snap
        ;;
      7)
        profile
        ;;
      *)
        echo "Invalid option!"
        echo "${OPT}"
        read_opt
    esac
  done
}

function stitch() {
  echo ""
  MSG="Stitcher options:\n\
0) Return to main\n\
1) Show corrected stitch\n\
2) Show cube map stitch\n\
3) Show sample stitch\n\
4) Show sample feed stitch"
  echo -e "${MSG}"
  read -p "Choose option: " OPT

  if [ "${OPT}" = 0 ]
  then
    read_opt
  fi

  cmd="${RUN_PACKAGE} ${STITCHER_DIR}.stitchexamples --option ${OPT}"
  eval "${cmd}"
  read_opt
}

function calibrate() {
  cmd="${RUN_PACKAGE} ${UTILITY_DIR}.calibrate"
  eval "${cmd}"
  read_opt
}

function flex() {
  cmd="${RUN_PACKAGE} ${FLEX_DIR}.flexor"
  eval "${cmd}"
  read_opt
}

function validate() {
  cmd="${RUN_PACKAGE} ${UTILITY_DIR}.validatefeeds"
  eval "${cmd}"
  read_opt
}

function capture() {
  echo ""
  MSG="Capture options:\n\
0) Return to main\n\
1) Capture single frame\n\
2) Catpure two frames\n\
3) Capture webcam\n\
4) Capture camera index 0\n\
5) Capture camera index 1\n\
6) Capture two videos"
  echo -e "${MSG}"
  read -p "Choose option: " OPT

  ARG=""
  case "${OPT}" in
    0)
      read_opt
      ;;
    1)
      ;;
    2)
      ARG="--cameras=2"
      ;;
    3)
      ARG="--type=video"
      ;;
    4)
      ARG="--type=video --cameras=1 --index=0"
      ;;
    5)
      ARG="--type=video --cameras=1 --index=1"
      ;;
    6)
      ARG="--type=video --cameras=2"
      ;;
    *)
      echo "Invalid option!"
      ;;
  esac

  cmd="${RUN_PACKAGE} ${UTILITY_DIR}.capture ${ARG}"
  eval "${cmd}"
  read_opt
}

function snap() {
  cmd="${RUN_PACKAGE} ${SNAPPER_DIR}.snapstreams --output out"
  eval "${cmd}"
  read_opt
}

function profile() {
  echo ""
  MSG="Profile options:\n\
0) Return to main\n\
1) Profile single stitch\n\
2) Profile two stitch"
  echo -e "${MSG}"
  read -p "Choose option: " OPT

  ARG=""
  case "${OPT}" in
    0)
      read_opt
      ;;
    1)
      ARG="--single"
      ;;
    2)
      ARG="--double"
      ;;
    *)
      echo "Invalid option!"
      ;;
  esac

  cmd="${RUN_PACKAGE} ${PROFILE_DIR}.profile ${ARG}"
  eval "${cmd}"
  read_opt
}

function main() {
  read_opt
}

main
