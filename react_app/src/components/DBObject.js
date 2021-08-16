import React from "react";
import { Card, Button } from "react-bootstrap";
import styled from "styled-components";
import Tilt from "react-tilt";
import { Link } from "react-router-dom";
import AllProducts from "../AllProducts";

const titles = [
  "Vlterri",
  "Vlterri",
  "Vlterri",
  "Vlterri",
  "Vlterri",
  "Vlterri",
  "Vlterri",
  "Vlterri",
];

const DBObject = ({ imgIdx, x, y, color }) => {
  const product = AllProducts.find((p) => p._id == imgIdx);

  const dboStyle = {
    boxShadow: "0px 13px 16px -13px black",
    border: `10px solid ${color}`,
    borderRadius: "3rem",
    margin: "1rem",
    position: "absolute",
    left: `${x}%`,
    bottom: `${y}%`,
    zoom: "30%",
  };

  return (
        <Link to={`/product/${imgIdx}`}>
          <TiltWrapper options={{ max: 5, scale: 1.1 }} style={dboStyle}>
            <StyledCard className="p-2">
              <StyledCardBody>
                <StyledTitle as="div">{product.name}</StyledTitle>
              </StyledCardBody>
              <StyledCardImg src={product.image}></StyledCardImg>
              {/* <Card.Footer as="div">{product._id}</Card.Footer> */}
              <Card.Footer as="div">{product.price}</Card.Footer>
            </StyledCard>
          </TiltWrapper>
        </Link>
  );
};

export default DBObject;

const TiltWrapper = styled(Tilt)`
  // margin: 1rem;
  // position: relative;
  // border: "3px solid red";
  // left: 0%;
  // bottom: 0%;
`;

const StyledText = styled(Card.Text)`
  text-align: left;
  &.text {
    font-size: 0.7rem;
    margin-bottom: 1.5rem;
    text-align: left;
  }
  &.price {
    display: flex;
    p {
        text-align: left;
        font-weight: 900;
        font-size: 2.7rem;
    }
    div { 
        div {
          margin-left: 0.2rem;
          &.dollar {
            margin-top: 0.7rem;
            font-weight: bold;
            font-size: 1rem;  
          }
          &.month {
            font-size: 0.7rem; 
          }
        }
      }
    }
  }
`;

const StyledTitle = styled(Card.Title)`
  font-weight: bold;
  font-size: 1.2rem;
  text-align: left;
`;

const StyledCardImg = styled(Card.Img)``;

const StyledCard = styled(Card)`
  // max-height: 200px;
  border-radius: 2rem;
  border: none !important;

  &.my-0.p-2.s {
    color: white;
    background-image: linear-gradient(
      to right,
      #ef2779 0%,
      #b42d9b 51%,
      #7834be 100%
    );
  }
  &.my-0.p-2.p {
    color: white;
    background-color: #ef2779;
  }
  text-align: center;
  vertical-align: middle !important;
  background-color: white;
  box-shadow: 0px 17px 10px 7px rgba(0, 0, 0, 0.7);
`;

const StyledCardBody = styled(Card.Body)`
  overflow: auto;
  margin-bottom: 0px;
  overflow: hidden;
  div {
    margin-bottom: 0px;
    overflow: hidden;
  }
`;

const StyledButton = styled(Button)`
  text-align: center;
  background-color: #ef2779;
  border-radius: 1rem;
  color: white;
  &:hover {
    background-color: #ef2779;
    box-shadow: 0px 10px 16px -11px black;
  }
`;
