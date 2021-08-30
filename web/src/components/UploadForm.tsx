import React, { useContext, useState } from 'react'
import { ThemeContext } from '../theme-context'



function UploadForm(props :any) {
  const { url, setUrl } = useContext(ThemeContext)
  const [upfile, setUpfile] = useState<File | undefined>()
  const [response, setResponse] = useState<string>('')
  const [isloading, setIsloading] = useState<boolean>(false)

  function handleFilePreview(e: React.ChangeEvent<HTMLInputElement> | null) {
    const fileList = e?.target.files;
    if (!fileList) {
      return
    }
    setUpfile(fileList[0])
  }

  async function handleClickSubmit(e: React.MouseEvent<HTMLButtonElement> | null) {
    setIsloading(true)

    const formData = new FormData()
    if (upfile) {
      formData.append('file', upfile)
    }

    const res = await fetch(`${process.env.REACT_APP_API_URL}/uploadfile/`, {
      "method": "POST",
      body: formData
    })

    let ret = await res.json()
    setResponse(ret)
    setIsloading(false)
    setUrl(`http://127.0.0.1:8000/items/${ret['hash_val']}?${Date.now()}`)
  }

  return (
    <div className="upload-form text-center mb-16">
      <div className="grid border-4 border-dashed border-gray-200 rounded-lg h-96" >
        <div className="place-self-center flex flex-col">
          <label className="block text-sm font-medium text-gray-700">
            Select file
          </label>
          <div className="mt-1 relative rounded-md">
            <div className="inset-y-0 right-0 flex flex-col items-center">

              <form className="flex" encType="multipart/form-data" method="post">
                <input name="files" type="file" onChange={handleFilePreview} />
                <button
                  className="py-2 px-4 bg-purple-600 text-white font-semibold rounded-lg shadow-md hover:bg-rose-700 focus:outline-none"
                  type="button"
                  onClick={handleClickSubmit}
                >
                  {
                    isloading ? (<div className="animate-spin inline-block">
                      <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M4 2a1 1 0 011 1v2.101a7.002 7.002 0 0111.601 2.566 1 1 0 11-1.885.666A5.002 5.002 0 005.999 7H9a1 1 0 010 2H4a1 1 0 01-1-1V3a1 1 0 011-1zm.008 9.057a1 1 0 011.276.61A5.002 5.002 0 0014.001 13H11a1 1 0 110-2h5a1 1 0 011 1v5a1 1 0 11-2 0v-2.101a7.002 7.002 0 01-11.601-2.566 1 1 0 01.61-1.276z" clipRule="evenodd" />
                      </svg>
                    </div>)
                    : null
                  }

                  <span>Submit</span>
                </button>
              </form>

              <p>{url}</p>

              <p>{JSON.stringify(response)}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default UploadForm
