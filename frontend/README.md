# RAG App Frontend

This is the frontend for the RAG (Retrieval-Augmented Generation) application. It is built using Angular and serves as the user interface for interacting with the backend API. The frontend allows users to upload documents, submit queries, and view retrieval-augmented responses.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [File and Component Explanations](#file-and-component-explanations)
- [Setup Instructions](#setup-instructions)
- [Running the Frontend](#running-the-frontend)
- [Available Scripts](#available-scripts)

---

## Prerequisites

Before running the frontend, ensure you have the following installed:

- **Node.js** (v14 or higher recommended): [Download Node.js](https://nodejs.org/)
- **npm** (comes with Node.js)
- **Angular CLI** (version 13.x):  
  Install globally if not already present:
  ```sh
  npm install -g @angular/cli@13
  ```

---

## Project Structure

```
frontend/
├── README.md
├── angular.json
├── package.json
├── tsconfig.json
├── tsconfig.app.json
├── tsconfig.spec.json
├── .angular/
│   └── cache/
├── src/
│   ├── index.html
│   ├── main.ts
│   ├── polyfills.ts
│   ├── styles.css
│   └── app/
│       ├── app.module.ts
│       ├── app.component.ts
│       ├── app.component.html
│       ├── app.component.css
│       └── ... (other components/services)
```

---

## File and Component Explanations

### Top-Level Files

- **README.md**: This documentation file.
- **angular.json**: Angular workspace configuration.
- **package.json**: Lists all Node.js dependencies and npm scripts.
- **tsconfig.json**: TypeScript compiler configuration.
- **tsconfig.app.json**: TypeScript configuration for the application code.
- **tsconfig.spec.json**: TypeScript configuration for unit tests.

### `.angular/` Directory

- **cache/**: Angular build cache (auto-generated, can be ignored).

### `src/` Directory

- **index.html**: The main HTML file loaded in the browser. Contains the `<app-root>` selector where the Angular app is rendered.
- **main.ts**: The entry point for bootstrapping the Angular application.
- **polyfills.ts**: Polyfills for browser compatibility.
- **styles.css**: Global styles for the application.

#### `app/` Directory

- **app.module.ts**: The root Angular module that declares and imports all components and services.
- **app.component.ts**: The root component containing the main logic and state for the application.
- **app.component.html**: The template for the root component, typically containing the main layout and router outlet.
- **app.component.css**: Styles specific to the root component.

> **Note:**  
> Additional components and services should be placed in this directory, such as:
> - **upload.component.ts/html/css**: Handles document upload UI and logic.
> - **query.component.ts/html/css**: Handles query submission and response display.
> - **api.service.ts**: Handles HTTP requests to the backend API.

---

## Setup Instructions

1. **Clone the Repository**

   ```sh
   git clone <repository-url>
   cd frontend
   ```

2. **Install Dependencies**

   Install all required Node.js packages using npm:

   ```sh
   npm install
   ```

   This will install:
   - Angular core and CLI packages
   - RxJS (reactive programming)
   - Zone.js (Angular change detection)
   - TypeScript and related build tools

---

## Running the Frontend

Start the Angular development server:

```sh
npm start
```
or
```sh
ng serve
```

- The app will be available at [http://localhost:4200](http://localhost:4200) by default.
- The frontend expects the backend API to be running (see backend README for instructions).

---

## Available Scripts

- **npm start** / **ng serve**: Start the development server with live reload.
- **npm run build** / **ng build**: Build the application for production in the `dist/` directory.
- **npm test** / **ng test**: Run unit tests.
- **npm run lint** / **ng lint**: Lint the codebase.
- **npm run e2e** / **ng e2e**: Run end-to-end tests.

---

## Implementation Overview

- **Document Upload**: Users can upload PDF or text files, which are sent to the backend `/upload` endpoint.
- **Query Submission**: Users can enter queries, which are sent to the backend `/query` endpoint. The response is displayed in the UI.
- **API Integration**: All HTTP requests are handled by a dedicated service (e.g., `api.service.ts`) using Angular's `HttpClient`.
- **Component-Based UI**: The UI is organized into reusable Angular components for upload, query, and results display.

---
