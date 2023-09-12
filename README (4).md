<a id="readme-top"></a>

<br>

<!-- table of contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#installation">How do I install Whale Clinc?</a></li>
    <li><a href="#running">How do I run Whale Clinic?</a></li>
  </ol>
</details>

<br>

<hr>

<br>

<a id="installation"></a>

# Installation

<br>

1. Download and install <a href="https://code.visualstudio.com/download">Visual Studio Code</a>.

2. Download and install <a href="https://desktop.github.com/">Github Desktop</a>.

3. Download and install git.
  
  npm install -g git
  

4. Clone the Home:Bound repository.
  sh
   gh repo clone SzeXinWei/ESD-ABC-Clinic
  

5. Launch GitHub Desktop and select the ESD-ABC-Clinic repository. 

6. Select the <b>singpass-apptbooking</b> branch.

7. Start WAMP/MAMP on your machine.

8. Start the Whale Clinic application by keying the following command into the terminal or command prompt. 
  
  npm run start
  

9. Access <b>localhost:3001</b> in your browser.

<br>

<a id="running"></a>

# Running

<p align="right">(<a href="#readme-top">back to top</a>)</p>

The following table describes our endpoints and their respective tasks:

<br>

<table>
  <thead>
    <th>Endpoint</th>
    <th>HTTP Methods</th>
    <th>Task</th>
  </thead>
  <tbody>
    <tr>
      <td>/medicine</td>
      <td>GET, POST</td>
      <td>Returns information about medicine inventory.</td>
    </tr>
    <tr>  
      <td>/medicine/admin</td>
      <td>GET, POST</td>
      <td>Returns information about medicine that is running low in stock.</td>
    </tr>
    <tr>  
      <td>/medicine/update</td>
      <td>GET, POST, PUT</td>
      <td>Creates a new medicine and add to medicine inventory.</td>
    </tr>
    <tr>  
      <td>/medicine/ < string:medicineName > </td>
      <td>PUT</td>
      <td>Updates information about an existing medicine in the medicine inventory.</td>
    </tr>
    <tr>  
      <td>/queue</td>
      <td>GET</td>
      <td>Returns information about patients in the queue.</td>
    </tr>
    <tr>  
      <td>/queue</td>
      <td>POST</td>
      <td>Adds a new patient to the queue.</td>
    </tr>
    <tr>  
      <td>/queue</td>
      <td>DELETE</td>
      <td>Removes a patient from the queue.</td>
    </tr>
    <tr>  
      <td>/appointment</td>
      <td>GET</td>
      <td>Returns information about all appointments.</td>
    </tr>
    <tr>  
      <td>/appointment/< int:appointmentID ></td>
      <td>GET</td>
      <td>Returns information about a specific appointment based on the appointment ID.</td>
    </tr>
    <tr>  
      <td>/appointment/< int:appointmentID ></td>
      <td>POST, PUT</td>
      <td>Creates a new appointment.</td>
    </tr>
    <tr>  
      <td>/schedule/ < int:doctorID ></td>
      <td>GET</td>
      <td>Returns information about schedules based on a specific doctor ID.</td>
    </tr>
    <tr>  
      <td>/schedule/ < int:doctorID > / < string:date ></td>
      <td>GET</td>
      <td>Returns information about schedules based on a specific doctor ID and date.</td>
    </tr>
    <tr>  
      <td>/schedule/update</td>
      <td>PUT</td>
      <td>Updates scheduling record.</td>
    </tr>
    <tr>  
      <td>/schedule</td>
      <td>GET</td>
      <td>Returns information about all schedules.</td>
    </tr>
    <tr>  
      <td>/patient/create</td>
      <td>POST</td>
      <td>Creates a patient and adds into database.</td>
    </tr>
    <tr>  
      <td>/patientRemoval</td>
      <td>GET, POST, PUT</td>
      <td>Removes patient from queue.</td>
    </tr>
    <tr>  
      <td>/payment</td>
      <td>GET</td>
      <td>Returns information about all payment records.</td>
    </tr>
    <tr>  
      <td>/payment/ < string: invoiceNo ></td>
      <td>GET</td>
      <td>Returns information about a specific payment record based on the invoice number.</td>
    </tr>
    <tr>  
      <td>/payment/amount/ < string: invoiceNo ></td>
      <td>GET</td>
      <td>Returns only the amount stated in a specific payment record based on the invoice number.</td>
    </tr>
  </tbody>
</table>

<br>

<p align="right">(<a href="#readme-top">back to top</a>)</p>