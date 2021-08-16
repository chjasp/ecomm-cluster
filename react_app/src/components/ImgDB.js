import React from "react";
import { Card, Button } from "react-bootstrap";
import styled from "styled-components";


const imgDB = (idx) => {
  return <StyledCardImg src="./images/0.jpg"></StyledCardImg>;
};

export default imgDB;

const StyledCardImg = styled(Card.Img)``;
