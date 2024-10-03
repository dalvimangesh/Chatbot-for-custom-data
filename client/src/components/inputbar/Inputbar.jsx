
function InputBar({ onSubmitHandler, buttonHandler, inputHandler, apiHandler }) {

    return (
        <>
            {

                // API Handler tells wheather we got unique key from flask server or not in GET request

                apiHandler ?
                    <form type="text" className="input-group w-100 inputbar mt-4 mb-3 ps-3 pe-3 pd-4" onSubmit={onSubmitHandler} >
                        {
                            <textarea type="text" className="form-control ms-2" rows={1} id="floatingTextarea"
                                ref={inputHandler} name='inputMsg' required
                            ></textarea>
                        }
                        <button className="btn btn-outline-success h-100 me-2" ref={buttonHandler} type='submit' id="button-addon2">Ask Question</button>
                    </form>
                    :
                    <div className="card info mb-5 ms-auto me-auto">
                        <div className="card-body">
                            <code> Oops! Our services are currently unavailable. 🙅‍♂️😕 Give it another shot or refresh the page. 🔄🔃 </code>
                        </div>
                    </div>
            }
        </>
    )
}

export default InputBar