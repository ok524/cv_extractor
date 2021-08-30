import React from 'react'

// Make sure the shape of the default value passed to
// createContext matches the shape that the consumers expect!
export const ThemeContext = React.createContext({
  url: '',
  theme: '',
  ajson: {
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
    status: '',
  },
  setUrl: (url :string) => {},
})

