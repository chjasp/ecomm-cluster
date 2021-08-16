import React from "react";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";
import { Navbar, Nav, Container, Row, NavDropdown } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";

const NavbarBS = () => {
  return (
    <StyledNavbar scrolling variant="dark" expand="md" fixed="top">
      <StyledNavBrand href="/">KREATION</StyledNavBrand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <StyledCollapse id="basic-navbar-nav">
        <StyledNav className="ml-auto">
          <StyledNavlink href="/">Premium</StyledNavlink>
          <StyledNavlink href="/">Profile</StyledNavlink>
          <StyledNavlink href="/">Cart</StyledNavlink>
        </StyledNav>
      </StyledCollapse>
    </StyledNavbar>
  );
};

export default NavbarBS;

const StyledNavBrand = styled(Navbar.Brand)`
  z-index: -11 !important;
  position: relative !important;
  color: black !important;
`;

const StyledNav = styled(Nav)`
  margin-right: 0px !important;
`;

const StyledCollapse = styled(Navbar.Collapse)`
  @media (max-width: 760px) {
    @supports (-webkit-backdrop-filter: none) or (backdrop-filter: none) {
      --webkit-backdrop-filter: blur(35px);
      backdrop-filter: blur(35px);
      backdrop-color: rgba(255, 255, 255, 0.4);
    }
  }
`;

const StyledNavlink = styled(Nav.Link)`
  color: black !important;
  margin-left: 6px;
  text-align: center;

  @media (max-width: 960px) {
    margin-left: 0px;
    margin-top: 0px;
  }

  &:hover {
    background-color: white;
    border-radius: 0.7rem;
    color: #0a0227 !important;
    -webkit-transition: background-color 0.3s;
    -webkit-transition: color 0.3s;
  }
`;

const StyledNavbar = styled(Navbar)`
  padding-left: 10%;
  padding-right: 10%;
  z-index: 20000;
  color: black;
  border-bottom: 1px solid black;
`;
