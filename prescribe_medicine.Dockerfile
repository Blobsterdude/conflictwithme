FROM python:3-slim 
WORKDIR /usr/src/app 
COPY http.reqs.txt ./ 
RUN python -m pip install --no-cache-dir -r http.reqs.txt 
COPY /prescribe_medicine.py ./amqp_setup.py ./
CMD [ "python", "/prescribe_medicine/prescribe_medicine.py" ]