import React, { useState, useEffect } from 'react'
import { ThemeContext } from './theme-context'
import Layout from './components/Layout'
import UploadForm from './components/UploadForm'
import Display from './components/Display'

import './App.css'

const APPURL = "http://127.0.0.1:8000/items/4a080aabcb383fcfd4bb18bbf69048e2"

interface ExampleObject {
  [key: string]: any;
  HardSkill: never[];
  SoftSkill: never[];
}

interface DataProperties {
  name: any;
  email: any;
  education: any;
  workExp: any;
  award: any;
  qualification: any;
  eca: never[];
  skillSets: ExampleObject;
}

interface MetaProperties {
  path_text: string;
  pdf_filename: string;
  text_filename: string;
}

interface StateProperties {
  text: any;
  meta: MetaProperties;
  data: DataProperties;
  status: string;
}

interface ContextProperties {
  url: string;
  theme: string;
  ajson: StateProperties;
  setUrl: (url :string) => void;
}

function App() {
  const [state, setState] = useState<ContextProperties>({
    "url": APPURL,
    "theme": 'light-theme',
    "ajson": {
      text: {},
      meta: {
        path_text: '',
        pdf_filename: '',
        text_filename: '',
      },
      data: {
        name: {text: ''},
        email: [],
        education: [{
          text: ''
        }],
        workExp: {},
        award: {},
        qualification: {},
        eca: [],
        skillSets: {
          HardSkill: [],
          SoftSkill: [],
        },
      },
      status: "",
    },
    setUrl: (url :string) => {
      updateUrl(url)
    },
  })

  function updateUrl(url :string) {
    setState({
      ...state,
      url: url
    })
  }

  useEffect(() => {
    async function anyNameFunction() {
      const res = await fetch(state.url)
      const ajson = await res.json()
      setState({
        ...state,
        ajson: ajson
      })
    }

    anyNameFunction()
  }, [state.url])

  return (
    <ThemeContext.Provider value={state}>
      <Layout>
        <UploadForm />
        <Display />
      </Layout>
    </ThemeContext.Provider>
  )
}

export default App
