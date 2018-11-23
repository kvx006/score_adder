# score_adder
Adds the scores in a table (in a cover sheet for an exam) when passing in an image of the table

To do:
Create (own) function which recognizes (handwritten) digit given a cell image from a table
Remove vertical and horizontal lines



Notes:
If cell has more than/less than two digits ?
Speed up by reducing resolution of image.


Done:
Orient table so table is upright
split image into cells
split cells into two subcell so that each subcell has a digit (works for some cases, but not for all) Works for more cases now
