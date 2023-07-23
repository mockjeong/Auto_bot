const puppeteer = require('puppeteer');

// Define your Telegram API token
const telgm_token = '5523286949:AAH-dLh7miR9gU9aMrGUZHOOLiuRlWHm0q4';

// Define your travel preset
const travel_preset = '1';

// Define your account information
const member_num = '0960000414';
const password = 'dbwjdahr11!';

let start, end, year, month, day, hours;

if (travel_preset === '1') {
  start = '서울';
  end = '양평';
  year = '2023';
  month = '5';
  day = '4';
  hours = '16';
} else {
  // Implement other presets or user input here
}

console.log("\n*****************************");
console.log("출발지 : " + start);
console.log("도착지 : " + end);
console.log("일  시 : " + year + "년 " + month + "월 " + day + "일 " + hours + "시");
console.log("위의 정보로 예매를 시작합니다.");

Reserve();

async function Reserve (){
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });

  await page.goto('http://www.letskorail.com/korail/com/login.do', { waitUntil: 'networkidle2' });

  await page.type('input[name="txtMember"]', member_num);
  await page.type('input[name="txtPwd"]', password);

  LoginButton = await page.waitForSelector('.btn_login', { timeout: 3000 });
  await LoginButton.click();

  await page.waitForNavigation({ waitUntil: 'networkidle2', timeout:3000 });

  const popupUrl = page.url();
  if (popupUrl.includes('popup')) {
    await page.close();
    const pages = await browser.pages();
    page = pages[0];
  }

  await new Promise(resolve => setTimeout(resolve, 2000));

  await page.goto('http://www.letskorail.com/ebizprd/EbizPrdTicketpr21100W_pr21110.do', { waitUntil: 'networkidle2' });

  await page.evaluate(() => {
    document.querySelector('#start').value = '';
    document.querySelector('#get').value = '';
  });
  await page.type('#start', start);
  await page.type('#get', end);
  await page.type('#s_year', year);
  await page.type('#s_month', month);
  await page.type('#s_day', day);
  await page.type('#s_hour', hours);

  SearchButton = await page.waitForSelector('.btn_inq', { timeout: 3000 });
  await SearchButton.click();

  let progress = 0;
  while (progress === 0) {
    await new Promise(resolve => setTimeout(resolve, 1000));

    const buttonType = await page.evaluate(() => {
      const Tbody = document.querySelector('tbody');
      const firstRow = Tbody.querySelector('tr.nth-child(1)');
      const fifthTd = firstRow.querySelector('td.nth-child(5) > a');
      return fifthTd ? fifthTd.alt : '';
    });

    if (buttonType === "예약하기") {
      // await page.click('td.sch_con2 > a');
      await new Promise(resolve => setTimeout(resolve, 5000));
      // Implement Telegram bot sendMessage here
      progress = 1;
      console.log("예매를 성공했습니다.");
    } else {
      try {
        await SearchButton.click();
      } catch (error) {
        // Handle error if any
      }
    }

    await new Promise(resolve => setTimeout(resolve, Math.random() * 1000 + 1000));
  }
}


  // Keep the browser open
  // await browser.close();