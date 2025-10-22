require 'PHPMailerAutoload.php';
$mail = new PHPMailer;
$mail->isSMTP();
$mail->Host = 'smtp1.example.com;smtp2.example.com';
$mail->SMTPAuth = true;
$mail->Username = 'user@example.com';
$mail->Password = 'secret';
$mail->SMTPSecure = 'tls';
$mail->From = 'from@example.com';
$mail->FromName = 'Mailer';
$mail->addAddress('whoto@example.com', 'John Doe');
$mail->addReplyTo('info@example.com', 'Information');
$mail->addCC('cc@example.com');
$mail->addBCC('bcc@example.com');
$mail->addAttachment('/var/tmp/file.tar.gz');
$mail->addAttachment('/tmp/image.jpg', 'new.jpg');
$mail->isHTML(true);
$mail->Subject = 'Here is the subject';
$mail->Body    = 'This is the HTML message body <b>in bold!</b>';
$mail->AltBody = 'This is the body in plain text for non-HTML mail clients';
if(!$mail->send()) {
    echo 'Message could not be sent.';
    echo 'Mailer Error: '. $mail->ErrorInfo;
} else {
    echo 'Message has been sent';
}