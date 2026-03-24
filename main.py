import prompts,generate_image,text_overlay,queries,db_conn
import logging
logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(message)s")

if __name__=='__main__':
    conn = None
    try:
        logging.info("Starting service...")
        verse,reference = prompts.return_verse() # llm endpoint caution
        logging.info(f"Selected verse: {reference}")
        prompt1=prompts.return_img_prompt1(verse) # llm endpoint caution
        logging.info("Bible prompt generated")
        logging.info("Prompt1: %s", prompt1)
        
        #prompt2=prompts.return_img_prompt2(verse) # llm endpoint caution
        prompt2=f"generate a image for this verse :{verse}. only image, Strictly no text on it."
        logging.info("Default prompt generated")
        logging.info("Prompt2: %s", prompt2)
        
        #image_bytes1 = generate_image.generate(prompt1)
        final_image_bytes1=generate_image.generate(prompt1)
        logging.info("Image 1 generated successfully")
        # final_image_bytes1 = text_overlay.generate_verse_image(image_bytes1,verse,reference)
        # logging.info("Image 1 text overlay successful")

        #image_bytes2 = generate_image.generate(prompt2)
        final_image_bytes2=generate_image.generate(prompt2)
        logging.info("Image 2 generated successfully")
        # final_image_bytes2 = text_overlay.generate_verse_image(image_bytes2,verse,reference)
        # logging.info("Image 2 text overlay successful")

        conn = db_conn.get_connection()
        logging.info("Connected to DB")
        queries.insert_success(conn,reference,verse,prompt1,prompt2,final_image_bytes1,final_image_bytes2)
        logging.info("Saved to DB")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        if conn:
            conn.rollback()

        conn = conn or db_conn.get_connection()

        queries.insert_error(conn,reference if 'reference' in locals() else None,verse if 'verse' in locals() else None,e)
        logging.info("Pushed error logs to DB")
    finally:
        if conn:
            conn.close()
            logging.info("DB connection Closed")
            logging.info("Job done")