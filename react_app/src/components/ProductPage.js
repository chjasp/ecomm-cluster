import React, { useState, useEffect } from "react";
import StarRatings from "react-star-ratings";
import { Link } from "react-router-dom";
import {
  Row,
  Col,
  Image,
  ListGroup,
  Button,
  Card,
  Form,
} from "react-bootstrap";
import styled from "styled-components";
import AllProducts from "../AllProducts"

const dboStyle = {
    zoom: "150%",
    maxHeight: "600px"
  }

function ProductPage({ match }) {
  const product = AllProducts.find((p) => p._id == match.params.id)
  return (
    <Container>
      <Row>
        <Col md={6}>
          <Image src={product.image} style={dboStyle} alt={product.name} fluid/>
        </Col>

        <Col md={3}>
          <ListGroup variant="flush">
            <ListGroup.Item>
              <h3>{product.name}</h3>
            </ListGroup.Item>

            <ListGroup.Item>
              <StarRatings
                rating={product.rating}
                starRatedColor="#ef2779"
                starDimension="15px"
                starSpacing="0px"
                numberOfStars={5}
                name="rating"
              />
            </ListGroup.Item>

            <ListGroup.Item>Price: {product.price}</ListGroup.Item>

            <ListGroup.Item>Description: {product.description}</ListGroup.Item>
          </ListGroup>
        </Col>

        <Col md={3}>
          <Card>
            <ListGroup variant="flush">
              <ListGroup.Item>
                <Row>
                  <Col>Status:</Col>
                  <Col>{1 > 0 ? "In Stock" : "Out of Stock"}</Col>
                </Row>
              </ListGroup.Item>

              <StyledListGroupItem>
                <StyledButton className="btn-block" type="button">
                  Add to Cart
                </StyledButton>
              </StyledListGroupItem>
            </ListGroup>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default ProductPage;

const StyledListGroupItem = styled(ListGroup.Item)`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`;

const StyledButton = styled(Button)`
  text-align: center;
  background-color: #ef2779;
  border-radius: 1rem;
  padding: 1em 0rem;
  width: 7rem;
  color: white;
  &:hover {
    background-color: #ef2779;
    box-shadow: 0px 10px 16px -11px black;
  }
`;

const Container = styled.div`
  width: 100%;
  margin-top: 10rem;
  margin-bottom: 0;
  display: flex;
  justify-content: top;
  align-items: center;
  flex-direction: column;
`;
