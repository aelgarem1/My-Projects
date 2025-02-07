
/* find the number of availalbe copies of the book (Dracula)      */

select count(*)
from Books
where title = 'Dracula'

/* check total copies of the book */
select count(*) - count(l.bookid) from Books b 
left join (select * from Loans where returneddate is null) l 
on b.BookID = l.BookID 
where b.title = 'Dracula' 


/* current total loans of the book */
-- your code

/* total available books of dracula */
-- your code


/*******************************************************/
/* Add new books to the library                        */
/*******************************************************/
Insert into Books values 
(2000, 'Alchemist', 'Paulo Coehlo', 2014, 123456788),
(2001, 'Biology', 'Coehlo', 2014, 123477788)


/*******************************************************/
/* Check out Books: books(4043822646, 2855934983) whose patron_email(jvaan@wisdompets.com), loandate=2020-08-25, duedate=2020-09-08, loanid=by_your_choice*/
/*******************************************************/
select * from Books where barcode in (4043822646, 2855934983)
select * from Patrons where email = 'jvaan@wisdompets.com'
insert into Loans ( loanid, bookid, patronid, loandate, duedate) values 
( 2001,11, 50, '2020-08-25', '2020-09-08'),
( 2002,93, 50, '2020-08-25', '2020-09-08')

select max(loanid) from Loans
--
/********************************************************/
/* Check books for Due back                             */
/* generate a report of books due back on July 13, 2020 */
/* with patron contact information                      */
/********************************************************/
select l.bookid, p.email from Loans l join Patrons p on l.patronid = p.patronid 
where duedate = '2020-07-13'

/*******************************************************/
/* Return books to the library (which have barcode=6435968624) and return this book at this date(2020-07-05)                    */
/*******************************************************/
select * from Books where barcode =6435968624
select * from Loans where bookid = 105 and returneddate is null
update Loans 
set returneddate = '2020-07-05'
where loanid = 1991


/*******************************************************/
/* Encourage Patrons to check out books                */
/* generate a report of showing 10 patrons who have
checked out the fewest books.                          */
/*******************************************************/
select l.patronid from Loans l join Patrons p on l.patronid = p.patronid
group by patronid
order by count(*) 
limit 10


/*******************************************************/
/* Find books to feature for an event                  
 create a list of books from 1890s that are
 currently available                                    */
/*******************************************************/
select distinct(title) from Books b 
where published between 1890 and 1899 and not exists 
(select * from Loans l where l.bookid = b.bookid and returneddate is null)

/*******************************************************/
/* Book Statistics 
/* create a report to show how many books were 
published each year.                                    */
/*******************************************************/
SELECT Published, COUNT(DISTINCT(Title)) AS TotalNumberOfPublishedBooks FROM Books
GROUP BY Published
ORDER BY TotalNumberOfPublishedBooks DESC;


/*************************************************************/
/* Book Statistics                                           */
/* create a report to show 5 most popular Books to check out */
/*************************************************************/
SELECT b.Title, b.Author, b.Published, COUNT(b.Title) AS TotalTimesOfLoans FROM Books b
JOIN Loans l ON b.BookID = l.BookID
GROUP BY b.Title
ORDER BY 4 DESC
LIMIT 5;
